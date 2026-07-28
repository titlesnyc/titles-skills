---
name: promo-pack
user-invocable: true
argument-hint: [campaign goal]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Generate a set of promotional campaign assets on TITLES (titles.xyz) in
  one artist's style — cover, social posts, banners, story crops — each
  sized for wherever the campaign runs. Use when the user wants marketing or
  promo visuals as a set: "promo pack", "campaign assets", "album promo",
  "launch visuals", "social media pack", "assets for my release", "marketing
  set", "cover plus socials". Asks the goal, then the style; explores a few
  artist models within a budget; iterates the direction with you; then
  produces the full set at the right aspect ratios and can add text or
  edits. Runs on the TITLES MCP — if TITLES tools are missing, connect
  mcp.titles.xyz/mcp first (see titles-setup). NOT for: a single image
  (generate-image), one edit to one image (edit-image), or a video set
  (motion-pack).
---

# promo-pack

One goal → a coordinated set of campaign assets in one artist's style, at the aspect ratios the campaign needs. Explore cheap, lock a direction, then produce the set.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill (connect `https://mcp.titles.xyz/mcp`, OAuth, free to start) and stop. Don't fall back to non-TITLES tools.

## 1. Goal first, then style — ask, never invent

Two asks, in order, and both are the user's to give — if either is missing, **ask and stop**. Don't infer a goal or a style from earlier conversation, and don't treat a category name as a brief.

1. **The goal / end product** — what the campaign is for and where it runs (a record release, a product launch, an event). This decides the asset list.
2. **The stylistic direction** — an artist, a reference, or a mood, in the user's words.

From the goal, decide the **asset list and aspect ratios**, and say them back. This is yours to judge from where the assets will live:
- A **record promo** typically wants **1:1** (cover), **4:5** (Instagram post), **16:9** (YouTube/site banner), **9:16** (story/reel).
- Other campaigns need different ratios — pick what fits the channels the user named. Don't force the record set onto a billboard or a web hero.

## 2. Find models + write the exploration prompt

`titles_search_models` with style + subject nouns from the goal and style (never guess model names — the catalog changes). Gather several fitting artist models, each with its `agent_description` / tags, artist name, and `model_url`.

Write **one** campaign prompt — the hero concept — that you'll run across all the models you explore, so the comparison is about the artist's style, not the prompt.

## 3. Budget → how many models to explore

Ask the user's **exploration budget**. Then probe one sample (step 4's first call) to get the real per-sample cost, and compute how many models fit: more budget = more models, but **cap around 5–6** (beyond that the comparison is noise) and floor at 2. Tell them: "at ~$X/sample, $BUDGET explores N models."

**The budget covers exploration only.** The final set and any edits are quoted and confirmed separately, later. Say so now so the number isn't mistaken for the whole job.

## 4. Explore — one sample per model

Generate **one** sample in each of the N models: the same exploration prompt, the same ratio (use the primary deliverable's ratio — usually 1:1 — so each sample doubles as a real cover candidate). Run one at a time on a shared `session_id`; the awaits afterward can run in parallel.

**Read `cost_usd` off each submit response** to track spend (older servers nest it as `cost_quote.total_usd` — read whichever comes back). Present the samples labeled by artist, each credited, via the canvas link and downloaded files (see **Delivery**).

## 5. Feedback rounds

Ask for feedback and iterate — adjust the prompt, swap a model, try more of a direction — **for as many rounds as the user wants**, until they're happy with one direction (a single model + prompt). Every round spends, so **state the running total each time** and flag before a round would pass the exploration budget.

## 6. Produce the full set

Direction locked. Now **quote the set separately**: project the chosen model's per-image cost across the asset list, per aspect ratio (cost scales with pixel count — a 1:1 runs richer than a 16:9/9:16). Show the total and get a go — this is fresh spend beyond exploration.

Generate each asset at its ratio in the locked model, **one subject per role** — hold the style constant (the model does that for free) and give each asset its own subject inside the same world, so the set is different images that belong together, not one image resized. One at a time, shared `session_id`, running cost reported. Deliver via canvas + downloads, and offer a feedback round on the set too.

## 7. Text & edits

When the set is right, ask if they want to **add text** (title, tagline) or **make edits**. If yes, ask which tier:

- **Higher quality (pricier) → Nano Banana Pro.** Resolve it live: `titles_search_models({ query: "nano banana", operator: "imgEditNode" })`. Best for text and precise edits — the right call for adding a title.
- **Budget → Seedream 5.0 Lite.** Resolve live: `titles_search_models({ query: "seedream lite", operator: "imgEditNode" })`.

Run the edit on the **selected final** as the base: `titles_edit_image({ output_id: <that final>, prompt: <only the change they asked for>, model_id: <resolved id> })`. The prompt describes the requested change and nothing else — name what stays. Report cost; iterate edits as asked.

## 8. Publish (offer)

Offer to publish selected finals to the TITLES feed with artist credit: `titles_publish`, showing the `name` + `description` first and getting the user's go. Offer it — don't assume — many promo assets are for off-platform use.

## Delivery — canvas + files

- **Always give the `session_url`** (the canvas). Raw output/CDN URLs 403 outside the browser.
- For the **files**, `titles_download_asset({ output_id, format })` returns a short-lived (~5 min), no-auth download URL:
  - **Shell host** (Claude Code / Codex): `curl` each to a named folder on disk and tell the user the path.
  - **Chat host** (claude.ai / mobile — no filesystem): hand them the link(s) to click before they expire; re-fetch if one lapses (cheap).

## Cost & etiquette

Every generation returns `cost_usd` on submit — keep a running total and remind the user at each gate and each feedback round. Within an approved budget, fire fast; don't re-ask per generation. One canvas link, the artist credited, the set laid out — no play-by-play between generations.

