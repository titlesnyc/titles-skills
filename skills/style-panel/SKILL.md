---
name: style-panel
description: |
  Explore one creative brief across several TITLES (titles.xyz) artists at
  once — a commission board. Use when the user is undecided on style or
  wants options: "show me this in a few styles", "which artist fits this",
  "give me options", "explore directions", "a few takes on [concept]",
  "compare artists for this". Picks 4–6 deliberately different artist
  models, generates the same concept through each, presents them side by
  side with artist credit, shows projected cost first, and hands the winner
  to drop-pack. Runs on the TITLES MCP — if TITLES tools are missing,
  connect mcp.titles.xyz/mcp first (see titles-setup). NOT for: generating
  in one known style (generate-image / drop-pack) or browsing artists
  without generating (find-artist).
---

# style-panel

One brief, several artists, side by side — the human picks the direction. The move only a multi-artist catalog can make.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Take the brief — never invent it

Get the concept (what to make) from the user. The whole point is divergence, so keep the concept fixed and let the artists vary — don't over-constrain.

**The concept is the user's to give. If it's missing, ask and stop** — don't infer one from earlier conversation or invent one because they said "show me options." Picking the *artists* is your job here; picking the *subject* is not.

## 2. Pick a diverse panel

`titles_search_models` and choose **4–6 deliberately different artists** — spread across style/mood/technique, not six variations on one look (run a couple of different queries to surface range). Divergence is the product: a panel of near-identical styles is a failed panel. Note each artist's name and `model_url`.

## 3. Quote the cost, then confirm

One probe generation, read `cost_quote.total_usd`, project across the panel (≈ per-image × panel size), show it, get a go or a cap. Single gate.

## 4. Generate one concept per artist

The **same concept prompt** through each artist's model (`titles_generate_image`, one `model_id` per call), one at a time on a shared `session_id`. Same subject and aspect ratio across the panel so the comparison is about *style*, not composition.

## 5. Present the board and route the winner

Show all directions together via the `session_url`, each labeled with its artist, credited. Make a recommendation but let the user pick. When they choose:
- **Build the full set in that style** → hand off to `drop-pack` with the chosen `model_id`.
- **Follow the artist** → `titles_set_following` so their work surfaces later.
- **More like this one** → a fresh panel of artists adjacent to the winner.

## Etiquette

Fire fast after the cost gate. Present the panel as a labeled comparison, one canvas link, a clear recommendation with reasons — never fake neutrality, pick a favorite and say why.
