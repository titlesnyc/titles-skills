---
name: vary-image
user-invocable: true
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Make fresh variations of an existing TITLES (titles.xyz) image — same idea,
  new takes — on a fixed pipeline, no model or prompt to pick. Use when the
  user says: "variations of this", "more like this one", "some alternates",
  "different takes on this", "riff on this image", "a few more options from
  this". Takes an image already on TITLES (its `output_id`) and an optional
  strength (how far to stray), and returns two new variations on the canvas.
  Runs on the TITLES MCP — if TITLES tools are missing, connect
  mcp.titles.xyz/mcp first (see titles-setup). NOT for: the exact same image
  again (rerun the source generation), a directed change (edit-image /
  restyle-image), or a new concept (generate-image).
---

# vary-image

New takes on an existing image — same idea, drawn from the image itself. Never ask for the original prompt, never search models.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Vary

One call: `titles_vary_image` with the image's `output_id`; `strength` sets how far the takes may stray. Cheap — if the user wants them looser or tighter, re-run at a different strength rather than explaining.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
