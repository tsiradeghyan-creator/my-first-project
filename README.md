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

## Firecrawl MCP Server

This repository is also configured to use the
[Firecrawl MCP server](https://github.com/firecrawl/firecrawl-mcp-server) via
`.mcp.json`. It lets Claude Code scrape, crawl, and extract structured data from
websites.

### Setup

1. Get an API key from [Firecrawl](https://www.firecrawl.dev/).
2. Export it in your shell before launching Claude Code:

   ```bash
   export FIRECRAWL_API_KEY="fc-your_key_here"
   ```

3. Start Claude Code in this directory and approve the `firecrawl-mcp` server.

> The API key is **not** stored in the repository — `.mcp.json` only references
> the `FIRECRAWL_API_KEY` environment variable.

### Optional environment variables

| Variable | Description |
| --- | --- |
| `FIRECRAWL_API_URL` | Self-hosted instance endpoint (overrides cloud API) |
| `FIRECRAWL_RETRY_MAX_ATTEMPTS` | Retry count (default: 3) |
| `FIRECRAWL_RETRY_INITIAL_DELAY` | First retry delay in ms (default: 1000) |
| `FIRECRAWL_RETRY_MAX_DELAY` | Maximum retry delay in ms (default: 10000) |
| `FIRECRAWL_CREDIT_WARNING_THRESHOLD` | Credit alert threshold (default: 1000) |

## Glif MCP Server

This repository is also configured to use the
[Glif MCP server](https://github.com/glifxyz/glif-mcp-server) via `.mcp.json`.
It lets Claude Code run [glif.app](https://glif.app) AI workflows (image
generation, text pipelines, and other community-built glifs).

### Setup

1. Get an API token from [glif.app/settings/api-tokens](https://glif.app/settings/api-tokens).
2. Export it in your shell before launching Claude Code:

   ```bash
   export GLIF_API_TOKEN="your-token-here"
   ```

3. Start Claude Code in this directory and approve the `glif` server.

> The token is **not** stored in the repository — `.mcp.json` only references
> the `GLIF_API_TOKEN` environment variable.

### Optional environment variables

| Variable | Description |
| --- | --- |
| `GLIF_IDS` | Comma-separated workflow IDs to auto-load |
| `IGNORE_DISCOVERY_TOOLS` | Set to `true` to disable discovery capabilities |
| `AGENT_TOOLS` | Set to `true` to enable agent functionality |

