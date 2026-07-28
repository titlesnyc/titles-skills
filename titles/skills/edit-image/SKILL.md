---
name: edit-image
user-invocable: true
argument-hint: [the change to make]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Edit an image on TITLES (titles.xyz) — change one thing, keep the rest. Use
  when the user says: "edit this image", "remove the background", "change the
  color of…", "add a hat", "replace the sky", "fix this part", "swap X for Y",
  "retouch this". Targeted, instruction-style edits: subject, composition, and
  style stay put while the requested change is applied. Works on images already
  on TITLES; returns a Studio canvas link plus a downloadable file. Runs on the
  TITLES MCP — if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: restyling the whole image (restyle-image), generating
  from scratch (generate-image), enlarging (upscale-image), or making video
  (animate-image).
---

# edit-image

Targeted changes to an existing image — "make her jacket red," "change the sky to sunset" — with everything else left alone.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get the image

`titles_edit_image` takes an `output_id` — an image already on TITLES:

- "this one" / "the one I picked" → `titles_get_selection` (explicit selection only — never resolve "the first one" from it; ask or list).
- Their recent work → `titles_list_outputs`; from the feed → `titles_search_feed` / `titles_get_feed_item`.
- Not on TITLES yet? An outside image can't be brought in via MCP — offer to generate one first (generate-image), or have them add it in the studio.

## 2. Edit

Call `titles_edit_image({ output_id, prompt, model_id?, session_id? })` — submit directly (cheap; don't pre-ask cost). Read `cost_usd` and mention it; handle `price_confirmation_required` by relaying the exact price, getting approval, then re-calling with `max_price_usd`.

- **Prompt is the instruction:** "make her jacket red", "remove the foreground customer", "change the sky to sunset". Name what stays as well as what changes.
- `model_id`: omit for a default fitted from the prompt (usually right); a specific edit model comes from `titles_search_models({ operator: "imgEditNode" })` — e.g. Nano Banana Pro for typography/precision, Seedream Lite for a cheaper pass.
- Reuse the source `session_id` so the edit lands on the same canvas. For a chain of edits, apply them one at a time and check the result between steps.
- If the user actually wants the whole image reinterpreted ("make it all watercolor"), hand off to **restyle-image**.

## 3. Deliver

- `titles_await_execution` → `titles_get_execution` for the finished output.
- The `session_url` (canvas) — raw output URLs 403.
- The file via `titles_download_asset({ output_id, format: "png" })` — host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

Run without asking twice. One link, one file, a short summary of what changed — no play-by-play.

