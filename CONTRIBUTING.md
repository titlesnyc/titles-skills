# Contributing to titles-skills

Public, external-facing skills for the **TITLES MCP** (`mcp.titles.xyz/mcp`),
packaged as a Claude plugin marketplace. Each skill wraps one TITLES creative
intent — generate/edit/restyle/upscale an image, make or transform video,
speech, music — so an agent can drive the TITLES tools correctly on a user's
behalf.

This is the **public** counterpart to the internal `titlesnyc/titles-internal-skills`
marketplace. Internal process/ops skills and the browser-driven Studio automation
(`*-tvbot`, prompter families) live there and are **not** mirrored here — this repo
is only the portable, pure-MCP tool-use skills anyone can install.

## Layout

```
.claude-plugin/marketplace.json        # lists every plugin (currently: titles)
.claude-plugin/plugin.json             # the titles plugin manifest
skills/<skill-name>/SKILL.md           # one skill; name in frontmatter == directory
SKILLS.md                              # the skill roster
scripts/validate_skills.py             # CI + local validation
.github/workflows/validate.yml         # runs the validator on push/PR
```

The `titles` plugin is the **repo root** (`"source": "./"` in `marketplace.json`),
so `skills/` sits at the top level rather than under a plugin subdirectory.

Keep it that way. `skills/` at the repo root is also the only path a Hermes skill
tap probes — `hermes skills tap add titlesnyc/titles-skills` hardcodes `skills/`
and its CLI has no flag to override it, so moving these under a subdirectory
silently produces an empty tap for every Hermes user. See "Hermes" in the README.

Adding a second plugin therefore means a sibling dir with its own
`.claude-plugin/plugin.json`, while `titles` keeps the root. If you ever need two
entries to share the root `skills/` folder, give each entry an explicit
`"skills": ["./skills/<name>", …]` list so it loads only its own.

## Adding a skill

1. **One job per skill.** Keep it narrow; compose by chaining, not by building
   mega-skills.
2. **Put it at `skills/<skill-name>/SKILL.md`** (repo root, not under `titles/`).
3. **Write the description for triggering.** Third person, specific, with explicit
   "Use when the user says…" trigger phrases and a closing `NOT for:` line that
   names the sibling skills it should defer to. With a library this size,
   description overlap is the #1 failure mode — every skill must be distinguishable
   from its neighbors by its description alone. Cross-reference only skills that
   actually ship.
4. **Respect the 1024-char description cap** (Anthropic hard limit). Long-tail
   keywords belong in a README, not the description.
5. **`name:` is required** and must match the directory — claude.ai zip upload has
   no directory-name fallback.
6. **Bump versions:** update the plugin's `version` in its `plugin.json` and the
   matching entry in `marketplace.json`.
7. **Add it to `SKILLS.md`.**
8. **No invisible unicode.** Zero-width and bidi characters score `high` in
   Hermes's skill scanner, and one high finding blocks install outright at
   community trust. The validator checks this.

## Frontmatter conventions

```yaml
---
name: generate-image
user-invocable: true
argument-hint: [subject + style]      # omit for skills that take no textual arg
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection
# (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning
# tools here would break portability across hosts.
description: >
  ...folded single-paragraph description with trigger phrases and a NOT-for line...
---
```

- **`description: >`** (folded) — reads as one flowing paragraph.
- **`user-invocable: true`** — these are things a user will also type directly
  (`/generate-image`), not only auto-triggered.
- **No `allowed-tools`.** Internal skills pin their tools because the environment
  is known; a public skill can't — the MCP server prefix differs per connection,
  and a pinned list silently blocks a validly-connected variant.

## Body conventions

- **Connect via `titles-setup`.** If the `titles_*` tools aren't present, hand off
  to the `titles-setup` skill and stop — don't inline per-client connect commands,
  and never fall back to a non-TITLES tool when the user asked for TITLES.
- **Resolve the catalog live.** Never bundle a static model/operator/price list —
  the catalog changes weekly. Use `titles_search_models`,
  `titles_resolve_input_constraints`, and `titles_list_operators` at runtime.
- **Cost.** Cheap runs (stills, audio) submit directly and report `cost_usd`.
  Anything that returns `price_confirmation_required` (typically video) must relay
  the exact price, get approval, then re-call with `max_price_usd` — never set
  `max_price_usd` without explicit approval.
- **Deliver both** the `session_url` (canvas — raw output URLs 403) and the file
  via `titles_download_asset`, host-adaptive.
- **No internal footers.** Draft copies in `titles-notion` carry a Notion spec
  footer; strip it before it lands here.

## Before you merge

- Run the validator: `python3 scripts/validate_skills.py`
- Benchmark triggering (e.g. `skill-creator`'s harness, or a routing test across
  the roster) so the new skill fires on its own intents and doesn't poach a
  sibling's.

## Validation

CI runs `scripts/validate_skills.py` on every push and PR. It enforces:

- `marketplace.json` + every `plugin.json` are valid, with matching names;
- every plugin dir on disk is listed in the marketplace;
- each plugin's `skills/` contains only skill directories (a loose file — a stray
  `.zip` especially — silently breaks claude.ai sync);
- every `SKILL.md` has frontmatter with `name:` (matching its directory) and
  `description:`, within the 1024-char cap;
- no committed junk (`.DS_Store`, `*.zip`, `*.skill`).
