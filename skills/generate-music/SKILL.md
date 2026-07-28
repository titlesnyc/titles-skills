---
name: generate-music
description: |
  Compose an original music track on TITLES (titles.xyz) from a text
  description. Use when the user says: "make music", "generate a track", "a
  beat", "background music for X", "an instrumental", "lofi for a podcast
  intro", "a jingle", "a song about Y". Describes genre / mood / instrumentation
  as a prompt; optional lyrics (sung verbatim) or instrumental-only; optional
  duration. Returns an audio track on the canvas. Runs on the TITLES MCP — if
  TITLES tools are missing, connect mcp.titles.xyz/mcp first (see titles-setup).
  NOT for: spoken narration or voiceover (text-to-speech), or sound on a video
  clip (animate-image with audio).
---

# generate-music

Text description → an original music track.

> Rolling out — `titles_generate_music` is on staging first. If it isn't in the tool list on this connection, tell the user music generation isn't available here yet.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Take the brief

Turn the user's idea into a `prompt` describing the **sound** — genre, mood, instrumentation, tempo ("mellow lofi for a podcast intro, rainy-night mood, tape hiss"). Two rules:
- **Describe the sound, not artists or labels.** Provider moderation hard-fails prompts that name real artists/songs — translate "sounds like [artist]" into the sonic qualities instead.
- **Lyrics vs instrumental:** put any words to sing in `lyrics` (used verbatim, lyrics-capable models only); set `instrumental: true` for no vocals. Ask which the user wants if it's a "song."

Set `duration` (numeric string of seconds, e.g. `"30"`) when the user wants a specific length; default is ~30s.

## 2. Generate

Call `titles_generate_music({ prompt, lyrics?, instrumental?, duration?, model_id?, session_id? })` — submit directly (don't pre-ask cost). Read `cost_usd` off the response and mention it; if it comes back `price_confirmation_required`, relay the price and re-call with an approved `max_price_usd`. `model_id` is optional — omit for the base music model unless the user wants a specific one (`titles_search_models({ operator: "txt2MusicNode" })`). Reuse `session_id` for related work.

## 3. Deliver

Audio has **no inline preview** — you can't "look" at it. `titles_await_execution` to confirm it finished, then:
- Point the user at the `session_url` to **listen**.
- Hand over the file with `titles_download_asset({ output_id, format: "mp3" })` (or `wav`), host-adaptive (disk on Claude Code/Codex, link on chat hosts).

## Etiquette

Submit, report the cost, deliver a listen link and a file. Don't describe how the music "sounds" — you can't hear it; let the user judge.
