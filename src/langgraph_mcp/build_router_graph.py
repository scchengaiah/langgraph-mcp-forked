import asyncio
import traceback

from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from langgraph_mcp import mcp_wrapper as mcp
from langgraph_mcp.configuration import Configuration
from langgraph_mcp.retriever import make_retriever
from langgraph_mcp.state import BuilderState


async def build_router(state: BuilderState, *, config: RunnableConfig):
    """
    Build the router by gathering routing descriptions from MCP servers and storing them in the retriever.

    Parameters:
        state (BuilderState): The current state of the router builder.
        config (RunnableConfig): The configuration for the router builder.

    Returns:
        dict: Status of the build process.
    """
    status = "failure"
    configuration = Configuration.from_runnable_config(config)
    mcp_servers = configuration.mcp_server_config["mcpServers"]

    try:
        # Gather routing descriptions directly without a shared dictionary
        routing_descriptions = await asyncio.gather(
            *[
                mcp.apply(server_name, server_config, mcp.RoutingDescription())
                for server_name, server_config in mcp_servers.items()
            ]
        )

        # Create documents from the gathered descriptions
        documents = [
            Document(page_content=description, metadata={"id": server_name})
            for server_name, description in routing_descriptions
        ]

        # Store the documents in the retriever
        with make_retriever(config) as retriever:
            if configuration.retriever_provider == "milvus":
                retriever.add_documents(
                    documents, ids=[doc.metadata["id"] for doc in documents]
                )
            else:
                await retriever.aadd_documents(documents)

        status = "success"
    except Exception as e:
        print(traceback.format_exc())
        print(f"Exception in run: {e}")

    return {"status": status}


builder = StateGraph(state_schema=BuilderState, config_schema=Configuration)
builder.add_node(build_router)
builder.add_edge("__start__", "build_router")
graph = builder.compile()
graph.name = "BuildRouterGraph"
