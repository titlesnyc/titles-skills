---
name: blend-images
description: |
  Blend two images into one on TITLES (titles.xyz) — merged on a fixed
  pipeline with a balance dial, no model or prompt to pick. Use when the user
  says: "blend these", "merge these two images", "combine these", "mix image A
  and B", "a 50/50 of these two", "cross these". Takes two images already on
  TITLES (their `output_id`s), an optional balance and aspect ratio, and
  returns the merged result on the canvas. Runs on the TITLES MCP — if TITLES
  tools are missing, connect mcp.titles.xyz/mcp first (see titles-setup).
  NOT for: a directed change to one image (edit-image), restyling one image
  (restyle-image), or generating from scratch (generate-image).
---

# blend-images

Merge two images into one. Fixed pipeline — no artist model, no prompt, so there's nothing to search or credit here.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get the two images

`titles_blend_images` takes two `output_id`s — images already on TITLES:
- "these two" / "blend the ones I picked" → `titles_get_selection` (returns `output_ids` in pick order; first = image 1).
- Their own recent work → `titles_list_outputs`. From the feed → `titles_search_feed` / `titles_get_feed_item`.
- Both images must already be on TITLES — bringing in an outside image isn't supported via MCP yet; add it in the studio first.

Confirm which image is 1 and which is 2 — the balance is directional.

## 2. Set the balance

`blend` is 0–100, default 50: lower leans toward image 1, higher toward image 2. Ask if the user has a lean; otherwise 50. `aspect_ratio` defaults to `1:1` — set it to match the use.

## 3. Blend

Call `titles_blend_images({ output_id_1, output_id_2, blend?, aspect_ratio?, session_id? })`. It's a single cheap call, so submit directly — don't pre-ask about cost. Read `cost_usd` off the response and mention it. If the run comes back `price_confirmation_required`, relay the exact price and only re-call with `max_price_usd` set to what the user approved. Reuse the source `session_id` so the blend lands on the same canvas. `titles_await_execution` → `titles_get_execution` for the inline preview.

## 4. Deliver

- The `session_url` (canvas) — raw URLs 403.
- The file via `titles_download_asset({ output_id, format: "png" })` — host-adaptive: `curl` to disk on Claude Code/Codex, click-link on chat hosts.

## Etiquette

One call, one result out (× the balance you chose). No model, so no artist credit line here — just the merged image and its cost.
