# Instructions

After following the `Development Setup` in [README.md](README.md), you can run the following commands to start the development server and open the LangGraph UI.

```bash
pip install -U "langgraph-cli[inmem]"

langgraph dev
```

1. `build_router_graph` is responsible to index the mcp servers into the vector database. Update `mcp servers` in the configuration named `mcp_server_config`. Refer to the [mcp-servers-config.sample.json](./mcp-servers-config.sample.json) for configuration reference. Replace the values wherever necessary.
2. `assistant_graph` takes in the user query and routes it to the appropriate mcp server. If no mcp server can address the query, it will return a message saying that it cannot address the query.
3. `assistant_graph_with_summarization` is similar to `assistant_graph` but it also summarizes the conversation history and stores it in the state. This is useful for long conversations where the agent needs to remember the context.