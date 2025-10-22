from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage 

from langchain_mcp_adapters.client import MultiServerMCPClient

from langgraph.graph.message import MessagesState
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import tools_condition,ToolNode

# from Schema import State

# call the api 
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

from langchain_core.globals  import set_llm_cache
from langchain_core.caches import InMemoryCache
set_llm_cache(InMemoryCache())


import asyncio


async def main():

    # Call the tools
    client = MultiServerMCPClient({
        "addition": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            "args": ["E:/Algorithm/LanggraphFastMCP/tools.py"],
            
        },

        "search_weather": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            "args": ["E:/Algorithm/LanggraphFastMCP/tools.py"],
            "env":{"TAVILY_API_KEY":TAVILY_API_KEY}
        },
    })

    # ✅ Await async call
    tools = await client.get_tools()

    llm= ChatGroq(model="openai/gpt-oss-120b")

    #Bind the tools and define the fuction to call the tools
    def model_call (state:MessagesState):

        Bind_llm =llm.bind_tools(tools).invoke(state["messages"])
        return {"messages":Bind_llm}
    #Define the Graph
    workflow =StateGraph(MessagesState)

    # Nodes
    workflow.add_node("Model",model_call)
    workflow.add_node("tools",ToolNode(tools))

    #Edges
    workflow.add_edge(START,"Model")
    workflow.add_conditional_edges("Model",tools_condition)
    workflow.add_edge("tools","Model")
    workflow.add_edge("Model",END)

    # Build the Graph
    agent =workflow.compile()
    

    # ✅ Invoke the agent
    response = await agent.ainvoke({
        "messages":"which is tools you have access?"})

    response=response["messages"][-1].content

    print("Response:", response)

if __name__ == "__main__":
    asyncio.run(main())

