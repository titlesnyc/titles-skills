---
name: style-explorer
user-invocable: true
argument-hint: [optional: a seed style or theme]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Roam the TITLES (titles.xyz) artist-model library — generate a wide, varied
  spread of images across many different artists and many different prompts to
  discover styles and directions. A survey, not a deliverable. Use when the
  user wants to explore or be shown range: "explore styles", "what styles are
  on TITLES", "surprise me", "show me a range", "wander the catalog", "what
  can this do", "discover artists by generating", "style exploration". Samples
  broadly across the catalog, presents the board grouped by look with each
  artist credited, and points at where to go deeper. Runs on the TITLES MCP —
  if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: producing a finished asset set (promo-pack),
  matching one artist without generating (find-artist), or browsing already-
  published feed work (curation-digest).
---

# style-explorer

Roam the TITLES artist library — a wide, varied spread of generations across many artists and many prompts, to discover what's possible. The point is *breadth*, not a decision.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop. Don't fall back to non-TITLES tools.

## 1. Frame the roam — a seed, not a brief

Exploration is the ask, so you don't need a concept and shouldn't demand one. Take whatever the user offers:
- **A loose seed** — a theme, medium, mood, subject area, or era ("something dreamlike", "3D creatures", "collage") — bias the roam toward it but keep wandering.
- **Nothing / "surprise me"** — sample across the catalog's whole range. This is valid here; generating varied prompts and picking styles yourself *is* the feature (the opposite of promo-pack, where inventing a brief is off-limits — there the user has a fixed output in mind; here they've asked to be shown range).

Settle only the breadth (how many images, or a budget) before spending.

## 2. Assemble a wide, diverse set of artists

`titles_search_models` — but the goal is **range, not the top of one query**. Run several different searches across style axes (painterly, 3D, collage, glitch, photographic, illustrative, abstract), and vary the sort (`popularity`, `recent`, `alpha`) so you surface artists a single query would bury. Aim for a spread of architecture, medium, and mood. Note each artist's name and `model_url`.

## 3. Budget → how wide to roam

Probe one generation, read `cost_usd` off the submit response (older servers nest it as `cost_quote.total_usd`). Ask the user's exploration budget, then compute how many (artist × prompt) samples fit — more budget = wider roam. Show the count and per-sample cost, get a go or a cap. Keep a running total and stop at the cap.

## 4. Roam — vary the artist AND the prompt

Generate a spread where **each sample is a different (artist, prompt) pairing**. Unlike a controlled comparison, here you vary both: let a collage artist get a collage-native prompt, a creature model get a creature, a landscape model a landscape — play to each model's strengths so the board shows what each artist actually does best, not one subject forced through all of them. One at a time, shared `session_id`. Look at each result (`titles_get_execution` inlines previews).

## 5. Present the survey and point deeper

Show the board via the `session_url`, **grouped by look/family**, each image credited to its artist with the `model_url`. For each cluster, a line on what's distinctive — the discovery is the map, not just the pictures. Then route the user onward:
- **Make something in a style that landed** → `generate-image` (one image) or `promo-pack` (a full asset set), passing that `model_id`.
- **Go deep on an artist** → `find-artist`, or `titles_set_following` to keep their work surfacing.
- **Roam further** → another spread, adjacent to whatever caught their eye, or off in a new direction.

## Etiquette

Fire fast within the approved budget — this is meant to be a wide, quick survey, not a labored one. One canvas link, the board grouped and every artist credited, and an honest read on what's worth chasing. Range is the deliverable; a spread of near-identical looks is a failed roam.

