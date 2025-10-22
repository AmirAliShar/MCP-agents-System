from fastmcp import FastMCP
from textwrap import shorten
from typing import Annotated

# initilize the server
mcp = FastMCP(name="CapstoneProject")

@mcp.tool()
def addition(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool(
          name="Summarizer_text",
          description ="Summarizes long text into a shorter version while keeping key meaning.")
def summarizer_text(
     text :Annotated[str,"User input Text"],
     max_len :Annotated[int,"Maximum length of the text to summarize"]
     ):
     """
    Summarize a given text to a specified maximum length.
    - text: The input content to summarize.
    - max_length: Desired summary length (default: 20 to 30 words).
    """
     if not text or len(text.strip()) ==0:
          raise ValueError("Text cannot be empty for summarization.")
    
     
     summary =shorten(text, width= max_len)
     return {
          "summary":summary
     }

from langchain_tavily import TavilySearch
@mcp.tool(
    name="Weather Tool",  # Custom tool name for the LLM
    description="Search the currnet weather condition with city name.", # Custom description
    tags={"catalog", "search"},      # Optional tags for organization/filtering
    meta={"version": "1.2", "author": "weather-team"}  # Custom metadata
)
def search_weather():
    """Internal function description (ignored if description is provided above)."""

    tavily_search_tool = TavilySearch(
    max_results=1,
    topic="weather",
   )
    return tavily_search_tool


@mcp.tool()
def translate_text():
 """Translate text between languages"""
 pass

@mcp.tool()
def analyze_sentiment():
     """Analyze emotional tone"""
     pass


@mcp.tool()
def fetch_weather():
    """Get weather info for a city"""
    pass

if __name__ == "__main__":
     mcp.run(transport="stdio")


"""

"""