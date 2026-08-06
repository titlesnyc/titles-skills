---
name: blend-images
user-invocable: true
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Blend two images into one on TITLES (titles.xyz) — merged on a fixed
  pipeline with a balance dial, no model or prompt to pick. Use when the user
  says: "blend these", "merge these two images", "combine these", "mix image A
  and B", "a 50/50 of these two", "cross these". Takes two images already on
  TITLES (their `output_id`s), an optional balance and aspect ratio, and
  returns the merged result on the canvas. Runs on the TITLES MCP — if TITLES
  tools are missing, connect mcp.titles.xyz/mcp first (see titles-setup).
  NOT for: a directed change to one image (edit-image), restyling one image
  (restyle-image), or generating from scratch (generate-image).
---

# blend-images

Merge two images into one. Fixed pipeline — no artist model, no prompt.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Blend

One call: `titles_blend_images` with the two `output_id`s. The balance is directional (image 1 vs image 2), so confirm which is which before leaning it.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
