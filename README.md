# TITLES Skills

Agent skills for the [TITLES](https://titles.xyz) MCP server — reusable instructions that teach coding agents (Claude Code, Codex, Cursor, and any other [agent-skills](https://github.com/vercel-labs/skills)-compatible agent) how to work with TITLES: connecting to the MCP, generating and editing images, discovering models, and publishing results.

## Install

```bash
npx skills add titlesnyc/titles-skills
```

This opens an interactive picker for the skills and agents on your machine. Or install everything non-interactively:

```bash
npx skills add titlesnyc/titles-skills --all
```

Target a specific agent:

```bash
npx skills add titlesnyc/titles-skills -a claude-code
```

## Skills

| Skill | What it covers |
|---|---|
| [`titles-setup`](./skills/titles-setup/SKILL.md) | Connecting your agent to the TITLES MCP server (`https://mcp.titles.xyz/mcp`), authenticating via OAuth, and verifying the connection |

More skills (image generation workflows, model discovery, publishing) are on the way.

## About the TITLES MCP server

The TITLES MCP server exposes the TITLES platform — AI image generation, model discovery, sessions, and publishing — over the [Model Context Protocol](https://modelcontextprotocol.io). It uses the Streamable HTTP transport with OAuth 2.1 (PKCE + dynamic client registration), so any modern MCP client can connect without pre-registered credentials.

- **Endpoint:** `https://mcp.titles.xyz/mcp`
- **Docs in-band:** once connected, call the `titles_help` tool for a full, example-shaped catalog of available tools

Tool behavior is defined by the server itself — these skills add workflow knowledge on top (setup, multi-step flows, conventions), and never override what the server tells your agent.

## License

[MIT](./LICENSE)
