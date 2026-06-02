# My First Project

This is my first project repository.

## Perplexity MCP Server

This repository is configured to use the [Perplexity MCP server](https://github.com/perplexityai/modelcontextprotocol)
via the project-scoped `.mcp.json` file. It exposes the `perplexity_search`,
`perplexity_ask`, `perplexity_research`, and `perplexity_reason` tools.

### Setup

1. Get an API key from the [Perplexity API portal](https://www.perplexity.ai/account/api).
2. Export it in your shell before launching Claude Code:

   ```bash
   export PERPLEXITY_API_KEY="your_key_here"
   ```

3. Start Claude Code in this directory. It will read `.mcp.json` and prompt you
   to approve the `perplexity` server on first use.

> The API key is **not** stored in the repository — `.mcp.json` only references
> the `PERPLEXITY_API_KEY` environment variable.

### Optional environment variables

| Variable | Description |
| --- | --- |
| `PERPLEXITY_TIMEOUT_MS` | Request timeout (default: 5 minutes) |
| `PERPLEXITY_BASE_URL` | Custom API endpoint |
| `PERPLEXITY_LOG_LEVEL` | Logging verbosity |
| `PERPLEXITY_PROXY` | Proxy configuration for corporate networks |

## Playwright MCP Server

This repository is also configured to use the
[Playwright MCP server](https://github.com/microsoft/playwright-mcp) via
`.mcp.json`. It lets Claude Code drive a real browser — navigate pages, click,
fill forms, take screenshots, and inspect the accessibility tree.

### Setup

No API key is required. The server is launched automatically via `npx`:

```
npx @playwright/mcp@latest
```

Requirements: Node.js 18 or newer. On first use, Claude Code will prompt you to
approve the `playwright` server.

