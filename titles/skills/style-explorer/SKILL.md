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
  can this do", "discover artists by generating", "what's new on TITLES",
  "show me new models", "style exploration". Samples
  broadly across the catalog, presents the board grouped by look with each
  artist credited, and points at where to go deeper. Runs on the TITLES MCP —
  if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: producing a finished asset set (promo-pack), or
  browsing already-published feed work (curation-digest).
---

# style-explorer

Roam the TITLES artist library — a wide, varied spread of generations across many artists and many prompts, to discover what's possible. The point is *breadth*, not a decision.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop. Don't fall back to non-TITLES tools.

## 1. Ask what they want to explore — specific first, breadth second

Exploration is the ask, so you don't need a full concept. **If they already gave a direction when they invoked the skill — a seed style/theme, "only new models", or "surprise me" — route on it, don't ask again.** Otherwise **ask whether they have something specific in mind** before defaulting to breadth. Either way, route on:
- **A particular style or direction** — a theme, medium, mood, subject, or era ("something dreamlike", "3D creatures", "art deco"). Bias the roam toward it across several artists, but keep wandering within it.
- **Only new / recent models** — they want to see what's just landed. Roam the newest additions via `titles_search_models({ sort: "recent" })`.
- **Specific artists or mediums** — center the roam on those and their neighbors.
- **No preference / "surprise me"** — *then* offer the full-breadth roam: sample across the catalog's whole range. Valid here; generating varied prompts and picking styles yourself *is* the feature (unlike promo-pack, where inventing a brief is off-limits — there the user has a fixed output in mind; here they've asked to be shown range).

Settle the breadth (how many images, or a budget) before spending.

## 2. Assemble a wide, diverse set of artists

Honor the step-1 focus: bias the searches to their style/direction, lead with `sort: "recent"` if they asked for new models, or sweep every axis for "surprise me". Either way the goal is **range, not the top of one query**: run several different searches across style axes (painterly, 3D, collage, glitch, photographic, illustrative, abstract), and vary the sort (`popularity`, `recent`, `alpha`) so you surface artists a single query would bury. Aim for a spread of architecture, medium, and mood. Note each artist's name and `model_url`.

## 3. Budget → price the ceiling first, then set breadth

Per-image cost varies **a lot** by architecture — a Nano Banana Pro or Flux sample can cost several times a Z-Image or Klein one. If you budget off the first (or cheapest) sample and extrapolate, you'll size the roam too generously and then have to **skip the expensive models mid-roam to stay in budget — which cuts exactly the diversity this skill exists for.** So price the ceiling before you talk breadth:

- **Find the top per-sample cost in your candidate set**, not the first. Reason from architecture (the pricier families cost multiples of the cheap ones), or probe the dearest-looking candidate and read `cost_usd` off its submit response (older servers nest it as `cost_quote.total_usd`).
- **Size the roam at that ceiling price** — ask the user's exploration budget, then compute how many samples fit *as if every one were the most expensive model*, so no pricey model has to be cut for cost.
- Show the count and the worst-case per-sample cost, get a go or a cap, and keep a running total. Because you priced the ceiling, the real spend usually lands under the estimate — say so when it does.

## 4. Roam — vary the artist AND the prompt

Generate a spread where **each sample is a different (artist, prompt) pairing**. Unlike a controlled comparison, here you vary both: let a collage artist get a collage-native prompt, a creature model get a creature, a landscape model a landscape — play to each model's strengths so the board shows what each artist actually does best, not one subject forced through all of them. One at a time, shared `session_id`. Look at each result (`titles_get_execution` inlines previews).

## 5. Present the survey and point deeper

Show the board via the `session_url`, **grouped by look/family**, each image credited to its artist with the `model_url`. For each cluster, a line on what's distinctive — the discovery is the map, not just the pictures. Then route the user onward:
- **Make something in a style that landed** → `generate-image` (one image) or `promo-pack` (a full asset set), passing that `model_id`.
- **Go deep on an artist** → `titles_set_following` to keep their work surfacing, or start creating in their style (`generate-image`).
- **Roam further** → another spread, adjacent to whatever caught their eye, or off in a new direction.

## Etiquette

Fire fast within the approved budget — this is meant to be a wide, quick survey, not a labored one. One canvas link, the board grouped and every artist credited, and an honest read on what's worth chasing. Range is the deliverable; a spread of near-identical looks is a failed roam.

