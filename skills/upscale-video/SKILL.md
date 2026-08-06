---
name: upscale-video
user-invocable: true
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Upscale a video on TITLES (titles.xyz) — make an existing clip
  higher-resolution and sharper. Use when the user says: "upscale this video",
  "make this clip higher-res", "enhance this video", "4k version of this clip",
  "sharpen this video", "clean up this footage". One call, no prompt. Works on a
  video already on TITLES; returns a Studio canvas link plus a downloadable file.
  Priced per clip and may clear the confirmation threshold, so the exact price is
  quoted for approval before anything runs. Runs on the TITLES MCP — if TITLES
  tools are missing, connect mcp.titles.xyz/mcp first (see titles-setup). NOT
  for: upscaling a still image (upscale-image), or making a new video
  (generate-video / animate-image / restyle-video).
---

# upscale-video

A sharper, higher-resolution version of an existing video clip.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Upscale

No dedicated tool for this one — it's the video upscale operator, `vidUpscaleNode`, via the generic path: `titles_get_operator({ operator_id: "vidUpscaleNode" })` for the live input shape, an upscaler from `titles_search_models({ operator: "vidUpscaleNode" })`, then `titles_run_execution`. No prompt — never regenerate to "upscale," that makes a different clip.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
