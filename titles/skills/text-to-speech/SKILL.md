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

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Take the text

The `text` is spoken **verbatim** — it's not a creative prompt, so pass exactly what the user wants said. Given a script, use it as-is; given a description, draft it and confirm the wording before spending (they're paying to hear their words, not your paraphrase).

## 2. Speak it

Two ways in, depending on what this connection exposes — submit directly either way (don't pre-ask cost):

- **Dedicated tool, if present:** `titles_generate_speech({ text, voice?, language?, speed?, model_id?, session_id? })` — resolves voice/language/speed server-side; omit them for the model's defaults.
- **Otherwise (the speech operator):** pick a voice model with `titles_search_models({ operator: "txt2SpeechNode" })`, then `titles_resolve_input_constraints({ operator_id: "txt2SpeechNode", adapter_id })` — it returns the allowed `voice`, `language`, and `speed` for that model (they're required, and don't carry across models). Pick from those (the user's choice, else a neutral default), then:
  ```
  titles_run_execution({
    operator_id: "txt2SpeechNode",
    inputs: { model: { model_id, adapter_id }, prompt: text, voice, language, speed },
    session_id?
  })
  ```
  (In the operator, the spoken text is the `prompt` input.)

Read `cost_usd` (speech is cheap — priced per character) and mention it; handle `price_confirmation_required` with the relay-approve-`max_price_usd` flow.

## 3. Deliver

No inline preview for audio. `titles_await_execution` to confirm completion, then:

- The `session_url` to **listen**.
- The file via `titles_download_asset({ output_id, format: "mp3" })` (or `wav`) — host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

Confirm the exact words before spending, submit, report cost, deliver a listen link and a file.

