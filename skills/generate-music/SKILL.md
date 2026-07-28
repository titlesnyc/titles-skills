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

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Take the brief

Turn the idea into a `prompt` describing the **sound** — genre, mood, instrumentation, tempo ("mellow lofi for a podcast intro, rainy-night mood, tape hiss"). Two rules:

- **Describe the sound, not artists or labels.** Provider moderation hard-fails prompts that name real artists/songs — translate "sounds like [artist]" into the sonic qualities instead.
- **Lyrics vs instrumental:** words to sing go in `lyrics` (used verbatim, lyrics-capable models only); instrumental-only sets `is_instrumental: true`. Ask which the user wants if it's a "song."

## 2. Run it

Two ways in, depending on what this connection exposes — submit directly either way (don't pre-ask cost):

- **Dedicated tool, if present:** `titles_generate_music({ prompt, lyrics?, instrumental?, duration?, model_id?, session_id? })` — resolves the model and duration server-side.
- **Otherwise (the music operator):** pick a model with `titles_search_models({ operator: "txt2MusicNode" })`, then `titles_resolve_input_constraints({ operator_id: "txt2MusicNode", adapter_id })` for the allowed `duration`, and call:
  ```
  titles_run_execution({
    operator_id: "txt2MusicNode",
    inputs: { model: { model_id, adapter_id }, prompt, duration, is_instrumental, lyrics? },
    session_id?
  })
  ```

Read `cost_usd` off the response and mention it; if `price_confirmation_required` comes back, relay the exact price, get approval, then re-call with `max_price_usd` (never set it without approval).

## 3. Deliver

Audio has **no inline preview** — you can't hear it, so don't describe how it sounds; let the user judge. `titles_await_execution` to confirm it finished, then:

- The `session_url` to **listen**.
- The file via `titles_download_asset({ output_id, format: "mp3" })` (or `wav`) — host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

Submit, report the cost, hand over a listen link and a file — don't narrate the sound.

