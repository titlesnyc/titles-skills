---
name: text-to-speech
user-invocable: true
argument-hint: [text to speak]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Turn text into spoken audio on TITLES (titles.xyz) — narration, voiceover,
  TTS. Use when the user says: "text to speech", "read this aloud", "voiceover
  for X", "narrate this", "TTS", "make this a voice clip", "say this in a
  voice". Speaks the text verbatim; optional voice, language, and speed. Returns
  an audio track on the canvas plus a downloadable file. Runs on the TITLES MCP —
  if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: music or singing (generate-music), or adding sound to
  a video clip (generate-video / animate-image with audio).
---

# text-to-speech

Literal text → spoken audio.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## Speak

The `text` is spoken verbatim, so pass exactly what the user wants said — given a description instead of a script, draft the wording and confirm it before spending (they're paying to hear their words, not your paraphrase). If they want a particular voice or delivery, match a voice model with `titles_search_models({ operator: "txt2SpeechNode" })` and pass its `model_id`; otherwise the one call `titles_generate_speech` lets the server pick a default voice.

You can't hear the result — hand over the listen link and let the user judge.

The connected server is authoritative for everything else — exact inputs, model resolution, cost approval (`price_confirmation_required` → `max_price_usd`), session/canvas handling, sourcing `output_id`s, and bringing outside images in (`titles_create_upload`) all follow the tool's own description and the server instructions, not anything memorized here. `titles_help` has the current catalog.

## Deliver the file

Besides the `session_url` the server points you at, hand over the actual file via `titles_download_asset` — host-adaptive: on a shell host (Claude Code / Codex) `curl` it to disk and give the path; on a chat host (claude.ai / mobile) give the short-lived link to click, re-fetching cheaply if it expires.
