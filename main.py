from fastmcp import FastMCP

from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
import getpass
import os

from dotenv import load_dotenv

load_dotenv()


db = SQLDatabase.from_uri("sqlite:///database.sqlite")
print(db.dialect)
print(db.get_usable_table_names())
res = db.run("SELECT * FROM Player LIMIT 10;")
print(res)


if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")


llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

mcp = FastMCP("MCP IPL Sql agent")

from langchain_community.agent_toolkits import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

print(tools)

system_message = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect="SQLite",
    top_k=5,
)

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

agent_executor = create_react_agent(llm, tools, prompt=system_message)

# query_player_stats: Player performance analytics
# match_analysis: Match-level insights and comparisons
# team_performance: Team statistics and trends
# season_comparisons: Cross-season analysis
# head_to_head: Team vs team historical data

def execute_query(question: str):

    for step in agent_executor.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()

@mcp.tool()
def query_player_stats():
    execute_query("get me the player stats for the player with the most runs in the last 5 years?")
    return "Player stats"

@mcp.tool()
def match_analysis():
    execute_query("get me the match analysis for the match with the most runs in the last 5 years?")
    return "Match analysis"

@mcp.tool()
def team_performance():
    execute_query("get me the team performance for the team with the most runs in the last 5 years?")
    return "Team performance"

@mcp.tool()
def season_comparisons():
    execute_query("get me the season comparisons for the season with the most runs in the last 5 years?")
    return "Season comparisons right ?"

@mcp.tool()
def head_to_head():
    execute_query("get me the head to head for the team with the most runs in the last 5 years?")
    return "Head to head"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)