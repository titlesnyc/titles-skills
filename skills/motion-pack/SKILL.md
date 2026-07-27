---
name: motion-pack
description: |
  Turn a TITLES (titles.xyz) artist's still images into a set of short
  motion loops. Use when the user wants animated art in an artist's style:
  "animate these", "make a motion pack", "a set of moving pieces", "loops
  for my drop", "bring this style to life". Generates or takes artist-style
  stills, animates each into a short clip, and delivers them as a set. Video
  is priced per second — shows the projected cost before running. Runs on
  the TITLES MCP — if TITLES tools are missing, connect mcp.titles.xyz/mcp
  first (see titles-setup). NOT for: a single still (generate-image), one
  animation (animate-image), or a still-image set (drop-pack).
---

# motion-pack

A set of short motion loops in one TITLES artist's style. Video is per-second and costs far more than stills — the cost gate matters here.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Take the brief and find the stills

Two entry points:
- **From existing stills** — the user's own outputs (`titles_list_outputs` or `titles_get_selection`) or a drop already made. Use those `output_id`s.
- **From a concept** — generate the stills first (this is `drop-pack`'s job; run it or its steps, then animate the keepers). Pick the artist via `titles_search_models`, credit them.

Settle how many loops (default 3) and the motion intent per still before running.

## 2. Pin one model + duration, then quote the cost

Pick **one** video model and **one** duration for the whole set and reuse them on every clip. If you let each call auto-fit (omit `model_id`/`duration`), the server picks a different model/length per prompt and the cost swings clip to clip — a single-clip probe then under-quotes the set, and the loops feel mismatched. Find a video model with `titles_search_models({ operator: "img2VidNode" })`; keep the duration short unless asked.

Then probe: animate **one** still with that fixed `model_id` + `duration`. `titles_await_execution` (several re-entries — video is slow; note `cost_quote` is populated while the clip is still `running`, so you can read the price before the render finishes). Read `cost_quote.total_usd`, project the set (per-clip × count — now representative because the model is pinned), and show it plainly: "3 clips ≈ $X.XX, video is per-second." Get an explicit go or a cap. Never skip this — motion-pack is the most expensive skill.

## 3. Animate the rest of the set

For each remaining still, `titles_animate_image({ output_id, prompt, model_id, duration, session_id })` — the **same** `model_id` + `duration` as the probe, and the shared `session_id` so the set lands on one canvas. `prompt` is the **motion** (camera move, subject action), not the scene — the still already carries the look. One at a time. Stop at the user's cap.

## 4. Deliver

Present the loops via the `session_url` (raw output URLs 403). Note that assembling them into one reel needs video concatenation, which isn't in the MCP yet — deliver as individual loops and say so. Offer to publish keepers.

## Etiquette

Fire after the cost gate, then stay quiet through the long renders — no play-by-play while waiting on video. One canvas link, the set, the artist credited.
