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
  (restyle-image), or upscaling (upscale-image).
---

# animate-image

Turn a still image into a short video clip — camera moves, subject motion, optional audio.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get the image

`titles_animate_image` takes an `output_id` — an image already on TITLES:

- "this one" / "the one I picked" → `titles_get_selection` (explicit selection only — never resolve "the first one" from it; ask or list).
- Their recent work → `titles_list_outputs`; from the feed → `titles_search_feed` / `titles_get_feed_item`.
- Not on TITLES yet? An outside image can't be brought in via MCP — generate the still on TITLES first (generate-image), then animate it.

## 2. Animate

Call `titles_animate_image({ output_id, prompt, duration?, audio?, model_id?, session_id? })`.

- **Prompt is the motion**, not the scene: "slow dolly-in as rain falls", "the cat turns its head and blinks". The image already provides the look.
- `duration` (string seconds, e.g. `"4"`, `"8"`) and `model_id` are model-specific — omit for defaults; a specific video model comes from `titles_search_models({ operator: "img2VidNode" })` (a video model, NOT the artist model the still was made with). An unsupported `duration` returns the allowed list.
- `audio: true` adds generated audio on models that support it (others return an error naming the limit). Default is silent.
- Reuse the source `session_id` so the clip lands on the same canvas.

Video clears the confirmation threshold, so expect **`price_confirmation_required`** back on the first call — that's the quote, nothing has run or charged. Relay the exact `cost_usd`, get the user's OK, then re-call the same tool with `max_price_usd` set to the approved amount (never set it without approval).

## 3. Deliver

- Video renders are long — expect several `titles_await_execution` re-entries before it finishes, then `titles_get_execution`.
- The `session_url` (canvas) — raw output URLs 403.
- The file via `titles_download_asset({ output_id, format: "mp4" })` — host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

One quote before spending, one clip out, its cost, the link and file. No play-by-play while it renders.

