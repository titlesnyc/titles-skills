# TITLES Skills

Agent skills for the [TITLES](https://titles.xyz) creative MCP — reusable
instructions that teach agents (Claude Code, claude.ai, Cowork, and any
MCP-capable Claude surface) how to work with TITLES: connecting to the MCP,
generating and editing images, video, and audio, discovering artist-trained
models, and running multi-asset creative packs.

Packaged as a Claude **plugin marketplace** with a single plugin, **`titles`**.

## Install (Claude Code)

```
/plugin marketplace add titlesnyc/titles-skills
/plugin install titles@titles-skills
```

That installs the whole `titles` skill set. On claude.ai / Cowork, an org admin
syncs this marketplace's plugin from **Org Settings → Skills**.

## Install (Hermes)

This repo doubles as a [Hermes](https://github.com/NousResearch/hermes-agent)
skill tap, because `skills/` sits at the repo root:

```
hermes skills tap add titlesnyc/titles-skills
hermes skills search titles
hermes skills install titlesnyc/titles-skills/skills/generate-image
```

`hermes skills check` and `hermes skills update` then track upstream changes per
skill (Hermes compares the content hash of each installed skill against this
repo — no version numbers involved). Skills install at `community` trust, so the
first install shows a third-party warning panel; all skills here scan clean, so
no `--force` is needed. Individual skills also install without adding the tap, by
passing the same `owner/repo/path` identifier.

## What's inside

The `titles` plugin bundles skills across images, video, audio, and creative
packs — see [`SKILLS.md`](./SKILLS.md) for the full roster. Start
with **`titles-setup`**; every other skill hands off to it when the TITLES tools
aren't connected yet.

## About the TITLES MCP server

The TITLES MCP server exposes the TITLES platform — AI image/video/audio
generation, model discovery, sessions, and publishing — over the
[Model Context Protocol](https://modelcontextprotocol.io). It uses Streamable
HTTP with OAuth 2.1 (PKCE + dynamic client registration), so any modern MCP
client can connect without pre-registered credentials.

- **Endpoint:** `https://mcp.titles.xyz/mcp`
- **In-band docs:** once connected, call the `titles_help` tool for a live,
  example-shaped catalog of available tools.

Tool behavior is defined by the server itself — these skills add workflow
knowledge on top (setup, model choice, cost handling, delivery) and never
override what the server tells your agent. The model and price catalog is
resolved live at runtime; nothing here hardcodes it.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). CI validates the marketplace on every
push and PR (`scripts/validate_skills.py`).

## License

[MIT](./LICENSE)
