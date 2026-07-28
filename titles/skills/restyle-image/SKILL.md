---
name: restyle-image
user-invocable: true
argument-hint: [target style]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Restyle an image on TITLES (titles.xyz) — reinterpret a whole image in a new
  style while keeping its subject, including running it through the style of an
  AI model trained by a real artist (credited and paid). Use when the user says:
  "restyle this image", "make this look like a painting", "in an artist's
  style", "turn this photo into an illustration", "apply a style", "style
  transfer", "make it watercolor / anime / film noir", "run this through a
  different model". Works on images already on TITLES; returns a Studio canvas
  link plus a downloadable file. Runs on the TITLES MCP — if TITLES tools are
  missing, connect mcp.titles.xyz/mcp first (see titles-setup). NOT for: creating
  a new image from text (generate-image), changing one part while the rest stays
  put (edit-image), enlarging (upscale-image), or making video (animate-image).
  To compare many artist styles at once, use style-explorer.
---

# restyle-image

Reinterpret a whole image in a new style — keeping its subject.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Restyle

One call: `titles_restyle_image` with the image's `output_id` and the target style as the prompt — restate the subject to keep, or the style swamps the content. Comparing many artist styles at once is **style-explorer**'s job — hand off rather than looping models here.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
