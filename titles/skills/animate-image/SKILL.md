---
name: animate-image
user-invocable: true
argument-hint: [the motion]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Animate an image on TITLES (titles.xyz) — turn a still into a short video clip.
  Use when the user says: "animate this image", "make this move", "image to
  video", "bring this to life", "turn this into a clip", "add motion to this".
  Describe the motion (camera move, subject action) and get a Studio canvas link
  plus a downloadable file; optional audio on supported models. Works on images
  already on TITLES. Video is priced per second and clears the confirmation
  threshold, so the exact price is quoted for approval before anything runs. Runs
  on the TITLES MCP — if TITLES tools are missing, connect mcp.titles.xyz/mcp
  first (see titles-setup). NOT for: creating a still (generate-image), making a
  video from text (generate-video), targeted edits (edit-image), restyling
  (restyle-image), or upscaling (upscale-image); for a SET of animated pieces,
  use motion-pack.
---

# animate-image

Turn a still image into a short video clip.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Animate

One call: `titles_animate_image` with the still's `output_id`; the prompt is the motion (camera move, subject action) — the image already provides the look.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
