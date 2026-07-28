---
name: restyle-video
user-invocable: true
argument-hint: [the change to make]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Transform an existing video on TITLES (titles.xyz) with a text prompt — change
  its subjects, look, or scene while keeping the motion. Use when the user says:
  "restyle this video", "change the style of this clip", "turn this video into
  X", "reimagine this footage", "change the scene / subject in this video",
  "video to video". Works on a video already on TITLES; returns a Studio canvas
  link plus a downloadable file. Priced per clip and clears the confirmation
  threshold, so the exact price is quoted for approval before anything runs. Runs
  on the TITLES MCP — if TITLES tools are missing, connect mcp.titles.xyz/mcp
  first (see titles-setup). NOT for: making a video from a still (animate-image)
  or from text (generate-video), or enlarging a video (upscale-video).
---

# restyle-video

Transform an existing video with a prompt — change its subjects, look, or scene, keeping the motion.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Transform

No dedicated tool for this one — it's the video-to-video operator, `vid2VidNode`, via the generic path: `titles_get_operator({ operator_id: "vid2VidNode" })` for the live input shape, a model from `titles_search_models({ operator: "vid2VidNode" })`, then `titles_run_execution`. The prompt is the change to make. Video-to-video quotes for approval before anything runs.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
