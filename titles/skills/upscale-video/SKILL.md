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

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get the video

This runs on a video output already on TITLES (its `output_id`):

- "this one" / "the clip I picked" → `titles_get_selection`.
- Their recent work → `titles_list_outputs`; from the feed → `titles_search_feed({ media_type: "video" })` / `titles_get_feed_item`.
- Not on TITLES yet? An outside video can't be brought in via MCP — make it on TITLES first (generate-video / animate-image).

## 2. Pick the upscaler

No dedicated tool — pick a video upscaler:

- `titles_search_models({ operator: "vidUpscaleNode" })` — each result carries the `{ model_id, adapter_id }` selector. This is an upscaler model, not the model the clip was made with.

## 3. Upscale

```
titles_run_execution({
  operator_id: "vidUpscaleNode",
  inputs: {
    video: { output_id },              // the clip to enlarge
    model: { model_id, adapter_id }    // from step 2
  },
  session_id?
})
```

No prompt — never regenerate to "upscale," that makes a different clip. If **`price_confirmation_required`** comes back, relay the exact `cost_usd`, get the user's OK, then re-call with `max_price_usd` (never set it without approval). Reuse `session_id`.

## 4. Deliver

- Renders take a while — several `titles_await_execution` re-entries, then `titles_get_execution`.
- The `session_url` (canvas) — raw output URLs 403.
- The file via `titles_download_asset({ output_id, format: "mp4" })` — host-adaptive.

## Etiquette

One clip out, its cost, link and file. No play-by-play while it renders.

