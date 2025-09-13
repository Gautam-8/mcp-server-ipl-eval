from fastmcp import FastMCP

from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
import getpass
import os


db = SQLDatabase.from_uri("sqlite:///database.sqlite")
print(db.dialect)
print(db.get_usable_table_names())
res = db.run("SELECT * FROM Player LIMIT 10;")
print(res)


if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")


llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

mcp = FastMCP("MCP IPL Sql agent")


# query_player_stats: Player performance analytics
# match_analysis: Match-level insights and comparisons
# team_performance: Team statistics and trends
# season_comparisons: Cross-season analysis
# head_to_head: Team vs team historical data

@mcp.tool()
def query_player_stats():
    return "Player stats"

@mcp.tool()
def match_analysis():
    return "Match analysis"

@mcp.tool()
def team_performance():
    return "Team performance"

@mcp.tool()
def season_comparisons():
    return "Season comparisons right ?"

@mcp.tool()
def head_to_head():
    return "Head to head"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)