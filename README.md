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

That installs the whole `titles` skill set.

### Updating

Third-party marketplaces
[don't auto-update by default](https://code.claude.com/docs/en/discover-plugins#configure-auto-updates)
(only Anthropic's official marketplaces do) — you stay on the version you
installed until you run:

```
/plugin marketplace update titles-skills
```

To pick up new releases automatically instead, enable auto-update for this
marketplace in your `~/.claude/settings.json` (or a project's
`.claude/settings.json` to opt a whole team in):

```json
{
  "extraKnownMarketplaces": {
    "titles-skills": {
      "source": { "source": "github", "repo": "titlesnyc/titles-skills" },
      "autoUpdate": true
    }
  }
}
```

## Install (claude.ai / Cowork)

No commands here — an org admin syncs this marketplace's plugin from
**Org Settings → Skills**, and everyone in the org gets the skills across
claude.ai, Cowork, and cloud sessions.

## Install (Codex)

Same flow, Codex-flavored:

```
codex plugin marketplace add titlesnyc/titles-skills
codex plugin add titles@titles-skills
```

`codex plugin list` shows what's installed;
`codex plugin remove titles@titles-skills` uninstalls.

> **The MCP server isn't bundled.** These skills drive the `titles_*` tools, and
> Codex loads MCP servers from `~/.codex/config.toml` (`[mcp_servers.titles]`) —
> connect it to `https://mcp.titles.xyz/mcp`, or start with the `titles-setup`
> skill, which walks the agent through it.
>
> ChatGPT itself has no skills mechanism — on the OpenAI side, skills run in
> Codex. (ChatGPT can still connect to the TITLES MCP directly.)

## Install (Cursor)

Cursor supports agent skills but not this plugin-marketplace flow — install
with the cross-agent [`skills` CLI](https://github.com/vercel-labs/skills)
(Node.js required):

```
npx skills add titlesnyc/titles-skills
```

It detects Cursor (and any other supported agent), lets you pick skills, and
installs all 18. Update later with `npx skills update`. The same command works
as a fallback for any agent the CLI supports — though on Claude Code and Codex,
prefer the plugin flow above, which can update through the marketplace.

> Same caveat: connect Cursor to the TITLES MCP separately
> (`.cursor/mcp.json` → `{ "mcpServers": { "titles": { "url": "https://mcp.titles.xyz/mcp" } } }`),
> or start with `titles-setup`.

## Install (Hermes Agent)

Add the repo as a skills tap, then install skills by name — Hermes discovers
the nested `titles/skills/<name>/` layout as-is:

```
hermes skills tap add titlesnyc/titles-skills
hermes skills install titlesnyc/titles-skills/titles-setup
hermes skills install titlesnyc/titles-skills/generate-image
# …repeat for the skills you want — full roster in titles/README.md
```

`hermes skills update <name>` pulls the latest;
`hermes skills uninstall <name>` removes one.

> Same caveat as Codex: Hermes resolves MCP servers from `~/.hermes/config.yaml`
> (`mcp_servers.titles`) — connect the TITLES MCP separately, or start with
> `titles-setup`.

## What's inside

The `titles` plugin bundles skills across images, video, audio, and creative
packs — see [`titles/README.md`](./titles/README.md) for the full roster. Start
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
