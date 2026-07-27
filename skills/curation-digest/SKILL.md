---
name: curation-digest
description: |
  Browse the TITLES (titles.xyz) feed, judge the best work in a style or by
  an artist, and save it to a collection with a short taste report. Use when
  the user says: "find the best X on TITLES", "curate a moodboard", "save
  some references", "what's good in [style]", "build me a collection", "show
  me strong work by [artist]". Searches the published feed, evaluates
  candidates visually, saves the keepers, and summarizes what makes them
  work. Mostly read-only — no generation cost. Runs on the TITLES MCP — if
  TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: generating new images (generate-image /
  drop-pack) or picking a model to create with (find-artist).
---

# curation-digest

Find the best work on the TITLES feed in a style, save it, and say why it's good. Near-zero cost — this is browsing and saving, not generating.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Frame the search

Get the target: a style ("analog collage", "low-poly retro"), an artist, or a subject — plus how many to save (default 8). Turn it into style + subject search terms, not a sentence.

## 2. Search the feed

`titles_search_feed` with those terms. Page with the returned cursor if you need a wider pool than the first response. Pull enough candidates to be selective — aim to look at 2–3× the target count before cutting.

## 3. Judge, don't just collect

Look at the candidates and pick on real criteria, not order: craft, coherence with the brief, and variety across the set (don't save six near-duplicates). For a finalist you're unsure on, `titles_get_feed_item` for detail. Credit the artist behind each pick.

## 4. Save the keepers

Save each keeper to the user's library with `titles_set_collection({ kind: "saved", target_id: <published_id>, state: true })` — `target_id` is the feed item's `published_id` (the `id` on the search result), not the `output_id`. TITLES has one saved library, not named per-brief collections, so the grouping is the report you write in step 5, not a container in the product. The response's `changed` tells you whether it was newly saved or already there.

## 5. Deliver the taste report

A short write-up *is* the collection: each pick with its artist credited (from the feed item's `owner.username`), its `published_url`, and one line per pick (or per cluster) on *why* it earned the spot. This grouped report is how the user (or a later `drop-pack` / `style-panel`) navigates the saves. Offer the next step — generate in this direction (`drop-pack`) or go deep on one artist (`find-artist`).

## Etiquette

No generation, no spend — so no cost gate. Be opinionated in the picks; a curation report that saves everything isn't curation.
