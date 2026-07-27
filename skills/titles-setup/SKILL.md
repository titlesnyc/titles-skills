---
name: titles-setup
description: Use when the user wants to connect their agent to TITLES, set up the TITLES MCP server, authenticate with TITLES, or when TITLES MCP tools are missing or returning authentication errors. Covers adding the server endpoint, the OAuth flow, verifying the connection, and troubleshooting.
---

# TITLES MCP Setup

Connect this agent to the TITLES MCP server so it can generate images, discover models, manage sessions, and publish results on [TITLES](https://titles.xyz).

## Server details

- **Endpoint:** `https://mcp.titles.xyz/mcp`
- **Transport:** Streamable HTTP
- **Auth:** OAuth 2.1 with PKCE and dynamic client registration (RFC 7591). No pre-registered client ID or API key is needed — MCP clients register themselves automatically and open a browser for the user to approve access with their TITLES account.
- **Discovery:** standard well-known documents are served at `https://mcp.titles.xyz/.well-known/oauth-authorization-server`.

## Add the server

Use the client's native MCP configuration. Examples for common agents:

**Claude Code**

```bash
claude mcp add --transport http titles https://mcp.titles.xyz/mcp
```

Then run `/mcp` inside Claude Code and select `titles` to complete the OAuth flow in the browser.

**Cursor** — add to `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

```json
{
  "mcpServers": {
    "titles": {
      "url": "https://mcp.titles.xyz/mcp"
    }
  }
}
```

**Other MCP clients** — any client that supports the Streamable HTTP transport with OAuth can connect. Configure a remote/HTTP MCP server with URL `https://mcp.titles.xyz/mcp`; the client handles registration and token exchange automatically. For clients that only support stdio servers, use a stdio→HTTP proxy such as `mcp-remote`:

```json
{
  "mcpServers": {
    "titles": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.titles.xyz/mcp"]
    }
  }
}
```

## Authenticate

The first connection triggers OAuth: a browser window opens on titles.xyz where the user logs in (or creates an account) and approves access. The client stores the resulting token and refreshes it automatically.

If no browser opens, tell the user to trigger authentication from the client's MCP UI (e.g. `/mcp` in Claude Code) rather than editing config by hand.

## Verify the connection

After setup, confirm the server is working:

1. Call `titles_get_me` — it should return the authenticated user's profile.
2. Call `titles_help` — it returns the full tool catalog with usage examples. Prefer this over guessing tool parameters.

## Troubleshooting

- **401 / "unauthorized" on every call** — the token is missing or expired and the client didn't refresh it. Re-run the client's authentication flow for the `titles` server (in Claude Code: `/mcp` → `titles` → re-authenticate).
- **Authentication succeeds but tools return permission/authorization errors** — the TITLES account may not have MCP access enabled yet. Ask the user to confirm their account has access; this is an account-level setting on TITLES, not a client problem.
- **Client says the server is unreachable** — check the URL is exactly `https://mcp.titles.xyz/mcp` (including the `/mcp` path) and the transport is HTTP/Streamable HTTP, not SSE-only or stdio.
- **Browser consent page loads but approval never completes** — third-party cookie blocking or an aborted login. Retry in the user's default browser, logged in to titles.xyz first.

## After setup

Lean on the server's own guidance: tool descriptions and `titles_help` are authoritative for parameters and behavior. Start read-only (`titles_get_me`, `titles_search_models`, `titles_search_feed`) before running executions that consume credits.
