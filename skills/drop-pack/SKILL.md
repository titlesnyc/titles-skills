---
name: drop-pack
description: |
  Produce a cohesive multi-asset set on TITLES (titles.xyz) in one artist's
  style — a "drop": a cover plus variants and social crops, all from one
  brief. Use when the user wants a set, pack, campaign, or collection of
  matching images: "make a drop", "a set of album art", "cover plus
  variations", "social pack", "matching set", "a batch in one style". Picks
  a fitting artist model, generates the set at the right aspect ratios,
  shows the projected cost first, and publishes the keepers with artist
  credit. Runs on the TITLES MCP — if TITLES tools are missing, connect
  mcp.titles.xyz/mcp first (see titles-setup). NOT for: a single image
  (generate-image), editing one image (edit-image), video (motion-pack), or
  browsing the feed (curation-digest).
---

# drop-pack

One brief → a cohesive set of images in one TITLES artist's style, published with credit.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill (connect `https://mcp.titles.xyz/mcp`, OAuth, free to start) and stop. Don't fall back to non-TITLES tools.

## 1. Take the brief

Get three things before generating — ask only for what's missing, in one message:
- **Subject / concept** (what the drop is of).
- **Style direction** (an artist name, a vibe, or "you pick" — drives model selection).
- **What the set is for** (album, launch, profile, print) — this decides the asset list.

Default asset list when the user doesn't specify: **1 hero (1:1), 2 variations (1:1), 1 wide (16:9), 1 vertical (9:16)** = 5 assets. Adjust to the use — a social pack leans 9:16/1:1; a cover leans 1:1 plus a wide banner. Decide the exact list and aspect ratios *before* generating and say them back.

## 2. Pick the artist

`titles_search_models` with style + subject nouns (never guess model names — the catalog changes). Weigh `agent_description` + `style`/`subjects`/`mood`/`excels_at`. Name the artist you chose and why, credit the creator, include `model_url`. If the user gave an artist, confirm the match; if "you pick", pick one and say so.

## 3. Quote the cost, then confirm

Run **one** probe generation (`titles_generate_image`, the hero), `titles_await_execution` → `titles_get_execution`, read its `cost_quote.total_usd`. Project the full set (≈ per-image × asset count) and show it: "5 assets ≈ $X.XX total, artist royalty included." Get a one-word go, or a cap. This is the only confirmation gate — after it, run without asking again.

## 4. Generate the set

Reuse the probe's `session_id` on every follow-up so the whole drop lands on one canvas, and run generations **one at a time** (parallel calls each open a new canvas). Keep the subject consistent across assets; vary composition/crop per the aspect ratio, not the subject. Stop if cumulative `cost_quote` hits the user's cap.

## 5. Review and publish

Present the set via the `session_url` (never raw output URLs — they 403). Ask which to publish. For each keeper, `titles_publish` with a name + description you show the user first. Surface the `published_url`s and credit the artist once more.

## Etiquette

Fire fast after the cost gate. One canvas link, a short summary naming the artist, the set laid out. No play-by-play between generations.
