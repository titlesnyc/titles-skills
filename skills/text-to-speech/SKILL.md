---
name: text-to-speech
description: |
  Turn text into spoken audio on TITLES (titles.xyz) — narration, voiceover,
  TTS. Use when the user says: "text to speech", "read this aloud", "voiceover
  for X", "narrate this", "TTS", "make this a voice clip", "say this in a
  voice". Speaks the text verbatim; optional voice, language, and speed.
  Returns an audio track on the canvas. Runs on the TITLES MCP — if TITLES
  tools are missing, connect mcp.titles.xyz/mcp first (see titles-setup). NOT
  for: music or singing (generate-music), or adding sound to a video clip
  (animate-image with audio).
---

# text-to-speech

Literal text → spoken audio.

> Rolling out — `titles_generate_speech` is on staging first. If it isn't in the tool list on this connection, tell the user speech generation isn't available here yet.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Take the text

The `text` is spoken **verbatim** — it's not a creative prompt, so pass exactly what the user wants said. If they gave you a script, use it as-is; if they described a message, draft it and confirm the wording before generating (they're paying to hear their words, not your paraphrase).

Optional, only when the user asks:
- `voice` — voice lists are **per-model** and don't overlap; omit for the model's default. An unsupported value errors with the options.
- `language` — omit or `"auto"` to auto-detect.
- `speed` — numeric string, e.g. `"0.9"` / `"1.2"`; omit for normal.

## 2. Generate

Call `titles_generate_speech({ text, voice?, language?, speed?, model_id?, session_id? })` — submit directly, don't pre-ask cost. Read `cost_usd` off the response; handle `price_confirmation_required` by relaying the price and re-calling with an approved `max_price_usd`. `model_id` optional (`titles_search_models({ operator: "txt2SpeechNode" })` for a specific one). Reuse `session_id` for related work.

## 3. Deliver

No inline preview for audio. `titles_await_execution` to confirm completion, then:
- Point the user at the `session_url` to **listen**.
- Hand over the file via `titles_download_asset({ output_id, format: "mp3" })` (or `wav`), host-adaptive.

## Etiquette

Confirm the exact words before spending, submit, report cost, deliver a listen link and file.
