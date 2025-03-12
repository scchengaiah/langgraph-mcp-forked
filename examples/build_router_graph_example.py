import asyncio
import json
import os
from dataclasses import asdict

from langgraph_mcp import build_router_graph
from langgraph_mcp.configuration import Configuration

# Get the project root directory (one level up from the current file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Now you can construct paths relative to the project root
# Example: if you need to reference a file in the project root:
config_file_path = os.path.join(PROJECT_ROOT, "mcp-servers-config.json")

with open(config_file_path, "r") as file:
    mcp_server_config = json.load(file)

input = {"status": "refresh"}
config = {"configurable": asdict(Configuration(mcp_server_config=mcp_server_config))}


async def main():
    response = await build_router_graph.ainvoke(input=input, config=config)
    print(response)


# Run the asynchronous main function
asyncio.run(main())
