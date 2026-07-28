---
name: restyle-video
description: |
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

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get the video

This runs on a video output already on TITLES (its `output_id`):

- "this one" / "the clip I picked" → `titles_get_selection`.
- Their recent work → `titles_list_outputs`; from the feed → `titles_search_feed({ media_type: "video" })` / `titles_get_feed_item`.
- Not on TITLES yet? An outside video can't be brought in via MCP — make it on TITLES first (generate-video / animate-image).

## 2. Pick the model

No dedicated tool — choose the video-edit model:

- `titles_search_models({ operator: "vid2VidNode" })` — never guess names; each result carries the `{ model_id, adapter_id }` selector. Credit the creator if it's an artist model.

## 3. Transform

```
titles_run_execution({
  operator_id: "vid2VidNode",
  inputs: {
    video: { output_id },              // the clip to transform
    model: { model_id, adapter_id },   // from step 2
    prompt                             // the change to make
  },
  session_id?
})
```

- **Prompt is the change** — "make it a snowy night scene", "turn the car into a horse", "1980s VHS look".
- Video-to-video clears the confirmation threshold, so expect **`price_confirmation_required`** back — the quote, nothing charged yet. Relay the exact `cost_usd`, get the user's OK, then re-call with `max_price_usd` (never set it without approval). Reuse `session_id`.

## 4. Deliver

- Renders take a while — several `titles_await_execution` re-entries, then `titles_get_execution`.
- The `session_url` (canvas) — raw output URLs 403.
- The file via `titles_download_asset({ output_id, format: "mp4" })` — host-adaptive.

## Etiquette

One quote before spending, one clip out, its cost, link and file. No play-by-play while it renders.

