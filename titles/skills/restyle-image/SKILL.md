---
name: restyle-image
user-invocable: true
argument-hint: [target style]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Restyle an image on TITLES (titles.xyz) — reinterpret a whole image in a new
  style while keeping its subject, including running it through the style of an
  AI model trained by a real artist (credited and paid). Use when the user says:
  "restyle this image", "make this look like a painting", "in an artist's
  style", "turn this photo into an illustration", "apply a style", "style
  transfer", "make it watercolor / anime / film noir", "run this through a
  different model". Works on images already on TITLES; returns a Studio canvas
  link plus a downloadable file. Runs on the TITLES MCP — if TITLES tools are
  missing, connect mcp.titles.xyz/mcp first (see titles-setup). NOT for: creating
  a new image from text (generate-image), changing one part while the rest stays
  put (edit-image), enlarging (upscale-image), or making video (animate-image).
  To compare many artist styles at once, use style-explorer.
---

# restyle-image

Reinterpret a whole image in a new style — "as a watercolor," "in this artist's style" — keeping its subject.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get the image

`titles_restyle_image` takes one `output_id` — an image already on TITLES:

- "this one" / "the one I picked" → `titles_get_selection` (explicit selection only — never resolve "the first one" from it; ask or list).
- Their recent work → `titles_list_outputs`; from the feed → `titles_search_feed` / `titles_get_feed_item`.
- Not on TITLES yet? An outside image can't be brought in via MCP — offer to generate one first (generate-image), or have them add it in the studio.

## 2. Restyle

Call `titles_restyle_image({ output_id, prompt, strength?, model_id?, session_id? })` — submit directly (cheap; don't pre-ask cost). Read `cost_usd` and mention it; handle `price_confirmation_required` by relaying the exact price, getting approval, then re-calling with `max_price_usd`.

- **Prompt is the target style** ("watercolor illustration", "gritty film noir") — restate the subject to keep ("keeping the two cats"), especially at higher strength, or the style swamps the content.
- **`strength`** runs `minimal → slight → moderate (default) → strong → extreme` — how far the result may drift from the source.
- **`model_id`**: omit for a default fitted from the prompt (usually right). To restyle into a specific artist's style, find it with `titles_search_models({ operator: "img2ImgNode" })` and credit the artist by name with their `model_url`.
- Reuse the source `session_id` so the restyle lands on the same canvas.

Comparing several artist styles at once is **style-explorer**'s job — hand off rather than looping models here.

## 3. Deliver

- `titles_await_execution` → `titles_get_execution` for the finished output.
- The `session_url` (canvas) — raw output URLs 403.
- The file via `titles_download_asset({ output_id, format: "png" })` — host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

Run without asking twice. One link, one file, short summary — no play-by-play.

