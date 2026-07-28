---
name: curation-digest
user-invocable: true
argument-hint: [optional: style or artist to focus]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Browse the TITLES (titles.xyz) feed, judge the best work in a style or by
  an artist, and save it to a collection with a short taste report. Use when
  the user says: "find the best X on TITLES", "curate a moodboard", "save
  some references", "what's good in [style]", "build me a collection", "show
  me strong work by [artist]". Searches the published feed, looks at the
  candidates, saves the keepers, and summarizes what makes them work.
  Mostly read-only — no generation cost. Runs on the TITLES MCP — if
  TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: generating new images (generate-image /
  promo-pack) or picking a model to create with (find-artist).
---

# curation-digest

Find the best work on the TITLES feed in a style, save it, and say why it's good. Near-zero cost — this is browsing and saving, not generating.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Frame the search

Get the target — a style ("analog collage", "low-poly retro"), an artist, or "what's good right now".

**Size the keep-count to the pool, don't fix it up front.** Curation is the cut: keep roughly half of what you look at, floor of 3. If a pool of 11 yields 8 saves you collected, you didn't curate. Tell the user the ratio in the report ("5 of 11").

## 2. Build the candidate pool

`titles_search_feed` does **not** take a free-text query — it filters by `model_id`, `username`, `media_type`, and remix flags, and sorts by `feature` or `date_created`. So route by target:

- **By style** → first `titles_search_models` with the style terms to get the artist models in that style, then `titles_search_feed({ model_id })` for each of the top matches. This is the main path; a style has no single feed query, it's a set of models.
- **By artist** → `titles_search_feed({ username })`.
- **"What's good" / a moodboard with no fixed style** → `titles_search_feed({ sort_by: "feature" })` for the featured pool.

**Keep `page_size` at 10 or less and page with the cursor.** Feed items are heavy (~4KB each — full asset metadata, avatars, embedded tool icons); `page_size: 20` on a prolific artist overflows the tool-result limit and dumps to a file. `media_type: "image"` (or `"video"`) narrows it.

## 3. Look at the work, then cut

**The feed tools return no images** — `titles_search_feed` and `titles_get_feed_item` give metadata only (unlike your own generations, which inline previews). To actually see a candidate, fetch its thumbnail from the public CDN and view it:

```
curl -sS -o cand.webp "<output.asset.thumbnail_url>"   # public, no auth
sips -s format jpeg -Z 420 cand.webp --out cand.jpg    # macOS; any converter works
```
Then read the file. Do this for every candidate before cutting — judging from titles and descriptions alone isn't curation.

Pick on craft, coherence with the brief, and variety (don't keep six near-duplicates). Common disqualifiers worth watching for: garbled hallucinated text where a model tried to render type, and compositions with unfilled gaps or unfinished edges. `titles_get_feed_item` adds the original prompt and an `is_saved` flag when you want more context on a finalist.

**Credit runs two layers deep on TITLES**, and both belong in the report: the **publisher** (`owner.username`) and the **model's artist** (`samples[].name` where `model_type` is `artist`) — often different people. When a piece is a remix, the source work's creator is a third credit, usually named in the description.

## 4. Save the keepers

Save each keeper to the user's library with `titles_set_collection({ kind: "saved", target_id: <published_id>, state: true })` — `target_id` is the feed item's `published_id` (the `id` on the search result), not the `output_id`. TITLES has one saved library, not named per-brief collections, so the grouping is the report you write in step 5, not a container in the product. The response's `changed` tells you whether it was newly saved or already there.

## 5. Deliver the taste report

A short write-up *is* the collection: the keep ratio ("5 of 11"), then each pick with both credits, its `published_url`, and one line on *why* it earned the spot — pointing at what's actually in the image, not the title. Say which ones were newly saved vs. already in the library (the `changed` flag). Name what you cut and why; the cuts prove the picks. Close with the pattern you noticed across the set — that's the part a list can't give them. Then offer the next step: generate in this direction (`promo-pack`), explore the range (`style-explorer`), or go deep on one artist (`find-artist`).

## Etiquette

No generation, no spend — so no cost gate. Be opinionated in the picks; a curation report that saves everything isn't curation.

If the user pivots from curating to *making* ("now generate one like these"), that.s `promo-pack` (make a set) or `style-explorer` (roam styles) — hand off rather than generating here, so the cost gate those skills carry isn't skipped.

