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

Targeted changes to an existing image — change one thing, keep the rest.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## 1. Get the edit, then match a model

Get the change they want and how exacting it is. Match a model to it with `titles_search_models({ operator: "imgEditNode" })` — text/typography or precise work wants a high-fidelity model (e.g. Nano Banana Pro), a quick change a cheaper one — and pass its `model_id`. If the ask is really a whole-image reinterpretation ("make it all watercolor"), hand off to **restyle-image**.

## 2. Edit

One call: `titles_edit_image` with the image's `output_id`, the chosen `model_id`, and the instruction as the prompt — name what stays as well as what changes.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
