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

## 1. Take the brief — never invent it

Three things before generating:
- **Subject / concept** — what the drop is actually of.
- **Style direction** — an artist, a reference, or a mood, in the user's words.
- **What the set is for** (album, launch, profile, print) — this decides the asset list.

**Subject and style are the user's to give. If either is missing, ask and stop.** Do not fill them in from the surrounding conversation, and do not treat "you pick" — least of all an option you wrote yourself — as license to invent a concept. A menu you authored is not the user's brief. Naming a category ("album cover set") is a *use*, not a direction: you still need to know what the record is.

If the user genuinely wants you to choose, make the choice concrete and theirs: search the live catalog and offer 3–4 real directions with the artist named ("Hybrid Garden by vitoriacribb — surreal humid biome, porcelain interiors"), then let them pick. Proposing options is right; assuming one is not.

The only things you may default are the asset list and aspect ratios below — those follow from the use, not from taste.

Default asset list when the user doesn't specify: **1 hero (1:1), 2 variations (1:1), 1 wide (16:9), 1 vertical (9:16)** = 5 assets. Adjust to the use — a social pack leans 9:16/1:1; a cover leans 1:1 plus a wide banner. Decide the exact list and aspect ratios *before* generating and say them back.

## 2. Pick the artist

`titles_search_models` with style + subject nouns (never guess model names — the catalog changes). Weigh `agent_description` + `style`/`subjects`/`mood`/`excels_at`. Name the artist you chose and why, credit the creator, include `model_url`. If the user gave an artist, confirm the match; if "you pick", pick one and say so.

## 3. Quote the cost, then confirm

Run **one** probe generation (`titles_generate_image`, the hero). **The submit response carries the run's cost immediately** — read `cost_usd` off it; you don't need to await the render to quote. (Older responses nested this as `cost_quote.total_usd` with a royalty breakdown; read whichever the server returns.)

**Cost scales with pixel count, so project per aspect ratio, not flat × N.** A square costs roughly 1.8× a 16:9 or 9:16 on the same model (observed: $0.055 vs $0.031 on Klein 9B). Multiply the probe by the number of assets *at that ratio*, then add the wide/vertical ones at their own rate — or quote the square rate across the board and tell the user it's the ceiling. Over-quoting is fine; under-quoting isn't.

Show the total ("5 assets ≈ $X.XX, artist royalty included"), get a one-word go or a cap. This is the only confirmation gate — after it, run without asking again.

## 4. Generate the set

Reuse the probe's `session_id` on every follow-up so the whole drop lands on one canvas, and run generations **one at a time** (parallel calls each open a new canvas — the awaits afterwards can run in parallel).

**Hold the style constant; vary the subject.** A drop is a set of *different images that belong together*, not one image at five sizes. Five crops of the same object is a failed drop — it reads as a template. Give each asset its own subject inside the same world: if the hero is the central object, let one variation change the object, one change the setting or scale, the wide one open onto the wider environment, the vertical one find a different form entirely. The artist model supplies the consistency for free — that's what it's for — so spend your prompt variety on *what's depicted*.

Stop if cumulative cost hits the user's cap.

## 5. Review and publish

Present the set via the `session_url` (never raw output URLs — they 403). Ask which to publish. For each keeper, `titles_publish` with a name + description you show the user first. Surface the `published_url`s and credit the artist once more.

## Etiquette

Fire fast after the cost gate. One canvas link, a short summary naming the artist, the set laid out. No play-by-play between generations.
