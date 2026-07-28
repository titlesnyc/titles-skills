---
name: generate-video
user-invocable: true
argument-hint: [scene + motion]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Generate a video on TITLES (titles.xyz) from a text description — a short clip
  built from a prompt, on a video model you pick from the catalog (some trained
  by real artists, credited and paid). Use when the user says: "generate a
  video", "make a video of…", "text to video", "a clip of…", "create a short
  video", "animate this idea" — or when the assistant can't make video itself.
  Describe the scene and motion; returns a Studio canvas link plus a downloadable
  file. Video is priced per second and clears the confirmation threshold, so the
  exact price is quoted for approval before anything runs. Runs on the TITLES MCP
  — if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: animating an existing still (animate-image),
  transforming an existing video (restyle-video), upscaling a video
  (upscale-video), or still images (generate-image).
---

# generate-video

Text to video on TITLES — describe a scene and get a short clip. For animating an existing still, use **animate-image** instead.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Generate

One call: `titles_generate_video` with the scene + motion as the prompt — the model, duration, resolution, and aspect ratio resolve server-side. Video is priced per second and quotes for approval before anything runs.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
