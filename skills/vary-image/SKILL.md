---
name: vary-image
description: |
  Make fresh variations of an existing TITLES (titles.xyz) image — same idea,
  new takes — on a fixed pipeline, no model or prompt to pick. Use when the
  user says: "variations of this", "more like this one", "some alternates",
  "different takes on this", "riff on this image", "a few more options from
  this". Takes an image already on TITLES (its `output_id`) and an optional
  strength (how far to stray), and returns two new variations on the canvas.
  Runs on the TITLES MCP — if TITLES tools are missing, connect
  mcp.titles.xyz/mcp first (see titles-setup). NOT for: the exact same image
  again (rerun the source generation), a directed change (edit-image /
  restyle-image), or a new concept (generate-image).
---

# vary-image

New takes on an existing image — same idea, drawn from the image itself. No model or prompt: never ask for the original prompt, never search models.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get the image

The tool takes one `output_id`:
- "this one" / "the one I picked" → `titles_get_selection`.
- Recent work → `titles_list_outputs`; from the feed → `titles_search_feed` / `titles_get_feed_item`.
- The image must already be on TITLES — bringing in an outside image isn't supported via MCP yet; add it in the studio first.

## 2. Set the strength

`strength` runs `minimal → slight → moderate (default) → strong → extreme` — how far the variations may stray from the source. Ask only if the user hinted at "close" vs "loose"; otherwise moderate.

## 3. Vary

Two ways in, depending on what this connection exposes — both submit directly (it's a cheap call, ~$0.009/output; don't pre-ask cost):

- **Dedicated tool, if present:** `titles_vary_image({ output_id, strength?, session_id? })`.
- **Otherwise (the variation operator):** `titles_run_execution({ operator_id: "imgVariationNode", inputs: { image: { output_id }, strength }, session_id? })`. Same operation, no model to pick. `strength` is required here — pass the value from step 2 (default `"moderate"`).

Either way: read `cost_usd` off the response and mention it; handle `price_confirmation_required` by relaying the price and re-calling with an approved `max_price_usd`. Reuse the source `session_id`. Then `titles_await_execution` → `titles_get_execution` for the inline previews.

## 4. Deliver

- The `session_url` (canvas).
- Files via `titles_download_asset({ output_id, format: "png" })`, host-adaptive (disk on Claude Code/Codex, links on chat hosts).

## Etiquette

A set of new takes per run (the dedicated tool returns two). If the user wants them looser or tighter, re-run with a different `strength` rather than explaining — one call is cheap.

