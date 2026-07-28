---
name: generate-video
description: |
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

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Pick the model

There's no dedicated tool — this runs through the generic execution path, so you choose the video model.

- `titles_search_models({ operator: "txt2VideoNode" })` — never guess model names. Some are artist-trained video models; if you pick one, credit the creator by name with their `model_url`. Each result carries the `{ model_id, adapter_id }` selector you pass as `model`.
- Weigh `agent_description` + tags for the look and motion the user wants.

## 2. Resolve the model's limits

Video inputs are model-specific. After picking, call `titles_resolve_input_constraints({ operator_id: "txt2VideoNode", adapter_id })` to get the allowed `duration`, `resolution`, and `aspect_ratio`. Choose from those — out-of-range values are rejected before anything runs.

## 3. Generate

```
titles_run_execution({
  operator_id: "txt2VideoNode",
  inputs: {
    model: { model_id, adapter_id },   // from step 1 — NOT model_architecture
    prompt,                            // the scene + the motion
    aspect_ratio,                      // from the resolved set
    duration,                          // from the resolved set (string seconds)
    resolution,                        // from the resolved set
    generate_audio                     // boolean; true adds a soundtrack on models that support it
  },
  session_id?
})
```

Video clears the confirmation threshold, so expect **`price_confirmation_required`** back on the first call — that's the quote, nothing has run or charged. Relay the exact `cost_usd`, get the user's OK, then re-call the same tool with `max_price_usd` set to the approved amount (never set it without approval). Reuse `session_id` to keep related clips on one canvas.

## 4. Deliver

- Video renders take a while — expect several `titles_await_execution` re-entries, then `titles_get_execution` for the finished clip.
- The `session_url` (canvas) — raw output URLs 403.
- The file via `titles_download_asset({ output_id, format: "mp4" })` — host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

One quote before spending, one clip out, its cost, the link and file. No play-by-play while it renders.

