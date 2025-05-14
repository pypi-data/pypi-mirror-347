from mcp.server.fastmcp import FastMCP, Context
import requests
from pydantic import Field
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

load_dotenv()

mcp = FastMCP(
    "YoutubeMusic", dependencies=["requests", "pydantic", "python-dotenv", "spotipy"]
)

# 1 first search for the song in spotify
# 2 then search for similar songs in spotify

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


@mcp.tool()
async def recommend_similar_songs(
    ctx: Context,
    song: str = Field(min_length=1, description="Song name to search for"),
    artist: str = Field(min_length=1, description="Artist name to search for"),
) -> any:
    """
    Get the song that is currently playing. Ask Cyanite to get the similar songs. show the result.
    """

    # Get the song id
    results = sp.search(q=f"track:{song} artist:{artist}", type="track", limit=1)
    if not results["tracks"]["items"]:
        await ctx.error("No song found in Spotify search")
        return {"success": False, "message": "No song found in Spotify search"}

    make_graphql_query = {
        "operationName": "SimilarTracksQuery",
        "variables": {"trackId": results["tracks"]["items"][0]["id"]},
        "query": """query SimilarTracksQuery($trackId: ID!) {\n  spotifyTrack(id: $trackId) {\n    __typename\n    ... on Error {\n      message\n    }\n    ... on Track {\n      id\n      similarTracks(target: { spotify: {} }) {\n        __typename\n        ... on SimilarTracksError {\n          code\n          message\n        }\n        ... on SimilarTracksConnection {\n          edges {\n            node {\n              id\n            }\n          }\n        }\n      }\n    }\n  }\n}""",
    }
    headers = {
        "Authorization": "Bearer " + os.getenv("CYANITE_ACCESS_TOKEN"),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = "https://api.cyanite.ai/graphql"
    response = requests.post(url, json=make_graphql_query, headers=headers)
    if response.status_code != 200:
        await ctx.error("error fetching data from Cyanite API")
        return {"success": False, "message": "error fetching data from Cyanite API"}

    data = response.json()
    if "errors" in data:
        await ctx.error("Error fetching data from Cyanite API")
        return {"success": False, "message": "Error fetching data from Cyanite API"}

    retrieved_similar_tracks = (
        data["data"].get("spotifyTrack", {}).get("similarTracks", {}).get("edges", [])
    )
    if not retrieved_similar_tracks:
        await ctx.error("No similar tracks found")
        return {"success": False, "message": "No similar tracks found"}

    similar_tracks = []
    for track in retrieved_similar_tracks:
        result = sp.track(track["node"]["id"])
        if not result or "id" not in result:
            continue
        track_data = {
            "name": result["name"],
            "artist": [artist["name"] for artist in result["artists"]],
            "album": result["album"]["name"],
            "preview_url": result["preview_url"],
            "external_url": result["external_urls"]["spotify"],
        }
        similar_tracks.append(track_data)

    return similar_tracks


def main():
    """Main entry point to run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
