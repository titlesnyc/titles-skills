---
name: upscale-image
user-invocable: true
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Upscale an image on TITLES (titles.xyz) — make it bigger and sharper. Use when
  the user says: "upscale this image", "increase the resolution", "make this
  higher-res", "enhance this image", "sharpen this", "make it print quality",
  "4k version of this". One call, no prompt needed. Works on images already on
  TITLES; returns a Studio canvas link plus a downloadable file. Runs on the
  TITLES MCP — if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: generating new images (generate-image), style changes
  (restyle-image), targeted edits (edit-image), or video (animate-image /
  upscale-video).
---

# upscale-image

A sharper, bigger, print-ready version of an existing image.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Upscale

One call, no prompt: `titles_upscale_image` with the image's `output_id`. Never re-generate to "upscale" — that makes a different image; upscaling keeps this one.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
