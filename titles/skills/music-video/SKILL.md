---
name: music-video
user-invocable: true
argument-hint: [the song / concept]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Turn a song into a music video on TITLES (titles.xyz): one character held
  across scenes, each scene animated, cut to the track. Use when the user says
  "make a music video", "turn this song into a video", "a lyric video", or "a
  music video for my track". Plans the scenes, generates or takes an artist-style
  hero, keeps the character consistent scene to scene (edit-image), animates each
  (animate-image), and scores to a supplied track or an original bed
  (generate-music) — delivering the clips and an ordered canvas sequence. An
  OPTIONAL local finisher (Claude Code + ffmpeg/Python, opt-in install) adds what
  makes it a real music video: beat and tempo detection, word-level lyric sync,
  lookbook + storyboard PDFs, and a beat-synced stitched render. Video is
  per-second — shows cost first. Runs on the TITLES MCP; if TITLES tools are
  missing, connect mcp.titles.xyz/mcp first (see titles-setup). NOT for: motion
  loops (motion-pack), a single clip (animate-image / generate-video), or a track
  alone (generate-music).
---

# music-video

A song → a character-driven, beat-cut music video. Two tiers, one skill:

- **Portable (pure MCP, any surface):** understand the song → plan the story → generate a
  hero and hold the character across scenes → animate each → score to a track → deliver the
  clips + an ordered canvas sequence.
- **Local finisher (Claude Code, opt-in):** the signature parts — precise beat/tempo
  detection, word-level lyric sync, a lookbook + storyboard PDF, and a beat-synced
  **stitched render**. Needs `ffmpeg` + a small Python venv; degrades gracefully off Claude Code.

Video is priced per second and costs far more than stills — the cost gate matters.

## The order matters: understand → treatment → footage

You can't write the story until you understand the song, and you can't shoot until the story
exists — so **understanding gates everything downstream, and footage is generated *to* a plan,
never the reverse.** Two entry paths, both of which end up analyzing a real track before the
plan locks:

- **Song-first (supplied track):** analyze + transcribe it, then reverse-engineer the treatment from it.
- **Story-first (no track yet):** form the concept, author the lyrics, let **`generate-music`**
  render the song (words known by construction), then **re-analyze the rendered track** for the
  exact beat/word timings before locking the treatment.

## Setup

- **MCP (required):** if the `titles_*` tools are missing, connect first — see `titles-setup`.
- **Local finisher (optional):** `bash scripts/setup.sh .mv-venv` (venv: numpy, demucs,
  faster-whisper, matplotlib, pillow); `ffmpeg` on PATH (`brew install ffmpeg`). Only needed
  for precise analysis, the PDFs, and the stitched render. Skip it and the skill runs MCP-only.

## Phase 0 — Preflight

`titles_get_me` (auth), confirm the account can spend, and settle the song: a supplied track,
or one from `generate-music` (instrumental, or a full vocal via its `lyrics`). Pick the entry
path above before generating anything.

## Phase 1 — Understand (before anything is generated)

Get the song's words and shape. **Local finisher:** `analyze_audio.py` (tempo, beat grid,
energy/section map) and `transcribe.py --isolate` (Demucs vocal → word-level timestamps →
`lyrics.json`). If the user already has the lyrics, use those; transcription is for the
timings. **MCP-only:** work from the provided lyrics and coarse sections by ear.

Read four signals: **structure** (intro/verse/chorus/bridge/drop = your act breaks),
**energy arc** (the emotional shape — where to hold vs. cut fast), **lyric imagery/theme**
(the world + per-line scene ideas), and **repetition** (the hook recurs → the video should
recur too).

## Phase 2 — Treatment (author the story from the song)

Synthesize a **beat sheet before any generation**: a through-line, a recurring character, a
**section → scene map** with timecodes, a **pacing plan** (long holds in verses, fast cuts +
the biggest scenes on the drop, a landing shot on the outro), and a **motif** that returns on
every chorus (what makes N clips feel like one film). This is the pre-`edit.json`.

```bash
.mv-venv/bin/python scripts/build_treatment.py analysis.json lyrics.json treatment.md "Title"
```
scaffolds the sheet (sections × timecodes × the lyric over each) with blank **Scene** and
**Motif** columns to fill. Generate footage to this sheet; don't retrofit a story onto random clips.

## Phase 3 — Footage (generate to the treatment)

1. **Hero + character consistency.** Generate the hero still (`generate-image`, one artist
   model), then hold the character **scene to scene** by editing it into each setting
   (`edit-image` — Nano Banana Pro excels at character-consistency). Lighter fallback: one
   `model_id` + a **verbatim character descriptor** in every prompt (see Craft rules).
2. **Review the stills before animating** — stills cost ~10× less than clips. Local:
   `build_lookbook_pdf.py`; MCP-only: review on the canvas. Approve/swap here.
3. **Animate** each approved still (`animate-image`), **pinning one video model + duration +
   aspect**. Continuity **clip to clip** via first-&-last-frame (previous clip's last frame →
   next start) or a **reference image** to re-ground the character. Optional `background_audio`
   for audio-reactive motion; `generate_audio` for per-clip foley (confirm via `titles_resolve_input_constraints`).
4. **Download:** `titles_download_asset({ output_id, format })`; `scripts/fetch.sh` is a
   local-only fallback.

## Phase 4 — Assemble

- **Portable:** hand back the clips + an **ordered canvas sequence** (reuse one `session_id`).
- **Local finisher:** `assemble.py edit.json` cuts to the treatment's grid (motion-onset trim,
  downbeat phase, favor-the-beat, stretch-only-when-forced), muxes the track, writes `edl.json`.
  Aspect configurable (`out_w/out_h/fit` → 9:16); clip lengths auto-probed.

## Phase 5 — Storyboard review

`build_review_pdf.py edl.json lyrics.json storyboard.pdf` — one row per shot (thumbnail · time ·
scene · lyric) — confirm the as-built cut matches the treatment; iterate without regenerating.
So there are **two storyboards**: the *treatment* (the plan, Phase 2) and this *as-built*
storyboard; the lookbook is the stills gate between them. Portable surfaces review the canvas sequence.

## Continuity techniques

- **Scene → scene (identity):** `edit-image` edit-from-hero (tightest); or one model + a
  verbatim descriptor (cheapest). Nano Banana Pro is the character-consistency workhorse.
- **Clip → clip (motion):** first-&-last-frame chaining; or reference-image video per clip.

## Finishing & extras

`upscale-video` for a crisp final (or `upscale-image` on the hero); `restyle-video` to unify a
look; a text-strong model for a **title card / lyric type**; `blend-images` for transitions.

## Craft rules

- **Motion can't animate a static pose** — bake the action into the still, then prompt the motion that continues it.
- **Character lock** = `edit-image` from a hero, or one model + a verbatim descriptor.
- **Pick the model by its tags** (`subjects` / `excels_at` / `style`); flux for busy scenes, sdxl reads storybook.
- **Distinct clips over reuse** — one clip per shot; if you must reuse, pull a different section, and budget for enough clips first.

## Cost

Every execution returns `cost_usd`; a run over the confirmation threshold returns
`price_confirmation_required` unless you pass an approved `max_price_usd`. Surface the clip
count and projected spend before a batch — video dominates the cost.

## Bundled scripts (local finisher)

`setup.sh` · `fetch.sh` · `analyze_audio.py` · `transcribe.py` · `build_treatment.py` ·
`assemble.py` · `build_review_pdf.py` · `build_lookbook_pdf.py` · `templates/edit.example.json`.
All opt-in; none run on a pure-MCP surface.
