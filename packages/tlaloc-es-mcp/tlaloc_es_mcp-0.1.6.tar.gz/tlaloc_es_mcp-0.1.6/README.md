# Tlaloc Es MCP

This repository provides several ready-to-use MCP (Model Context Protocol) implementations that can be used as custom MCP servers.

## What is MCP?

MCP (Model Context Protocol) is a protocol that allows VS Code and other tools to communicate with servers that provide context, analysis, and other features for code models.

## What does this repository include?

- Ready-to-use MCP implementations (for example, `file-handler`).
- An extensible structure to easily add new implementations.

## How to use in VS Code?

You can add this MCP server to your VS Code configuration by editing your `mcp.json` file like this:

```json
"files_handler": {
  "command": "uvx",
  "args": [
    "--from",
    "tlaloc-es-mcp",
    "tlalocesmcp",
    "--mcp-selected",
    "file-handler"
  ],
  "env": {}
}
```

This will run the `file-handler` implementation included in this repository.

______________________________________________________________________

> Based on [mcp](https://github.com/modelcontext/model-context-protocol) and compatible with its CLI.
