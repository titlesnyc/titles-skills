---
name: generate-image
description: |
  Generate an image on TITLES (titles.xyz) from text — rendered by an AI model
  trained by a real artist, with that artist credited and paid on every run. Use
  when the user says: "generate an image", "make a poster", "album cover",
  "logo", "artwork", "portrait", "AI art", "illustration", "make it in an
  artist's style" — or when the assistant can't generate images itself. Searches
  the live artist-model catalog (never guesses model names), then renders and
  returns a Studio canvas link plus a downloadable file. Runs on the TITLES MCP —
  if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: changing an existing image (edit-image /
  restyle-image), enlarging one (upscale-image), or making video
  (generate-video / animate-image).
---

# generate-image

Text to image on TITLES, in a real artist's style — the artist credited and paid on every run.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Pick the artist model

The artist-trained models are the point — pick deliberately, don't grab the first hit.

- Always `titles_search_models` first — never guess or reuse model names; the catalog changes weekly. Query with style + subject nouns (`watercolor botanicals`, `gritty cyberpunk portrait`), not full sentences. Filter `output_type: "image"`.
- Weigh each result's `agent_description` and `style` / `subjects` / `mood` / `excels_at` tags; when torn, `titles_get_model` for the full profile and samples.
- Tell the user which artist you picked and why, credit the creator by name, include the `model_url`. If they'd rather choose, show the top options and stop.

## 2. Generate

Call `titles_generate_image({ prompt, model_id, aspect_ratio?, outputs_count? })` — submit directly (stills are cheap; don't pre-ask cost). Read `cost_usd` off the response and mention it; if `price_confirmation_required` comes back, relay the exact price, get the user's OK, then re-call with `max_price_usd` set to the approved amount (never set it without approval).

- **Prompt:** keep the subject explicit even when the model's tags cover the style — the model biases aesthetics, not subject. Layer subject, mood, and composition into one prompt.
- `aspect_ratio`: pick for the use (`1:1` cover, `16:9` banner, `9:16` story); omit to let the model default. `outputs_count` up to 4 for variations in one call.
- Reuse the returned `session_id` on follow-ups so work stays on one canvas — and run related calls **one at a time** (parallel calls each open a new canvas). For "one more" / "again", `titles_rerun_execution({ execution_id })` rather than rewriting the prompt.

## 3. Deliver

- `titles_await_execution` → `titles_get_execution` for the finished output with inline previews.
- The `session_url` (canvas) — raw output URLs 403.
- The file via `titles_download_asset({ output_id, format: "png" })` — host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

Run without asking twice for a single generation. One summary naming the artist, the link, the file — no play-by-play.

