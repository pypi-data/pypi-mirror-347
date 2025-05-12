# Mock Ads MCP Server

This project provides a test MCP server for ads campaign management, using the [fastmcp](https://github.com/jlowin/fastmcp) framework. It is intended for development and testing purposes only.

## Running locally

```bash
uv run mock_ads_mcp
```

or with the MCP inspector for debugging

```bash
npx @modelcontextprotocol/inspector uv run src/mock_ads_mcp/test_ads_mcp_server.py
```

## Deploy