import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool(name, {})
        print(result)

async def call_all_tools():
        await call_tool("query_player_stats")
        await call_tool("match_analysis")
        await call_tool("team_performance")
        await call_tool("season_comparisons")
        await call_tool("head_to_head")


if __name__ == "__main__":
   asyncio.run(call_all_tools())
