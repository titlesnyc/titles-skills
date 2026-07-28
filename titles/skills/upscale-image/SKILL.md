---
name: upscale-image
user-invocable: true
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Upscale an image on TITLES (titles.xyz) — make it bigger and sharper. Use when
  the user says: "upscale this image", "increase the resolution", "make this
  higher-res", "enhance this image", "sharpen this", "make it print quality",
  "4k version of this". One call, no prompt needed. Works on images already on
  TITLES; returns a Studio canvas link plus a downloadable file. Runs on the
  TITLES MCP — if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: generating new images (generate-image), style changes
  (restyle-image), targeted edits (edit-image), or video (animate-image /
  upscale-video).
---

# upscale-image

A sharper, bigger, print-ready version of an existing image.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get the image

`titles_upscale_image` takes an `output_id` — an image already on TITLES:

- "this one" / "the one I picked" → `titles_get_selection` (explicit selection only — never resolve "the first one" from it; ask or list).
- Their recent work → `titles_list_outputs`; from the feed → `titles_search_feed` / `titles_get_feed_item`.
- Not on TITLES yet? An outside image can't be brought in via MCP — offer to generate one first (generate-image), or have them add it in the studio.

## 2. Upscale

Call `titles_upscale_image({ output_id, model_id?, session_id? })` — that's the whole call, no prompt. Submit directly; read `cost_usd` and mention it; handle `price_confirmation_required` by relaying the exact price, getting approval, then re-calling with `max_price_usd`.

- **Never re-generate to "upscale"** — that makes a different image. Upscaling keeps this one.
- `model_id`: omit for the default upscaler (usually right). A specific upscaler comes from `titles_search_models({ operator: "imgUpscaleNode" })` — note it's an upscaler model, NOT the artist model the image was made with.
- Reuse the source `session_id` so the result lands on the same canvas.

## 3. Deliver

- `titles_await_execution` → `titles_get_execution` for the finished output.
- The `session_url` (canvas) — raw output URLs 403.
- The file via `titles_download_asset({ output_id, format: "png" })` — host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

Run without asking twice. One link and one file out — no play-by-play.

