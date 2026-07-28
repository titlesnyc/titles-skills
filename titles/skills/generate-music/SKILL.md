---
name: generate-music
user-invocable: true
argument-hint: [genre / mood / instrumentation]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Compose an original music track on TITLES (titles.xyz) from a text
  description. Use when the user says: "make music", "generate a track", "a
  beat", "background music for X", "an instrumental", "lofi for a podcast
  intro", "a jingle", "a song about Y". Describes genre / mood / instrumentation
  as a prompt; optional lyrics (sung verbatim) or instrumental-only; optional
  duration. Returns an audio track on the canvas plus a downloadable file. Runs
  on the TITLES MCP — if TITLES tools are missing, connect mcp.titles.xyz/mcp
  first (see titles-setup). NOT for: spoken narration or voiceover
  (text-to-speech), or sound on a video clip (generate-video / animate-image
  with audio).
---

# generate-music

Text description → an original music track.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Compose

Get the brief — genre, mood, instrumentation, tempo — described as the **sound**, not artists or labels (provider moderation hard-fails prompts naming real artists/songs, so translate "sounds like [artist]" into sonic qualities). If they want a particular model for genre fit or lyric support, match one with `titles_search_models({ operator: "txt2MusicNode" })` (they differ on genre strengths and whether they sing lyrics) and pass its `model_id`; otherwise omit `model_id` and let the server pick a default. Then the one call, `titles_generate_music`, with that brief as the prompt; words to sing go in `lyrics`; ask lyrics-vs-instrumental if it's a "song."

You can't hear the result — don't describe how it sounds; hand over the listen link and let the user judge.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
