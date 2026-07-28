---
name: generate-image
user-invocable: true
argument-hint: [subject + style]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
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
  (generate-video / animate-image); for a full multi-asset campaign set, use
  promo-pack.
---

# generate-image

Text to image on TITLES, in a real artist's style — the artist credited and paid on every run.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## 1. Get their idea, then match a model

Ask what they have in mind — a subject, a style, an artist, a reference — if they haven't already said; don't invent a direction for them. Then match it: `titles_search_models` on their style + subject terms, weigh the results' style/subject tags, and pick the best-fitting artist model (the artist-trained models are the point — don't just grab the first hit). Surface the pick and credit the artist.

## 2. Generate

Hand the chosen `model_id` to the one call, `titles_generate_image`. Keep the subject explicit in the prompt; the model biases aesthetics, not content.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
