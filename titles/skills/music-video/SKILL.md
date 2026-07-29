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

- **Portable (pure MCP, any surface):** plan scenes → generate a hero and hold the
  character consistent → animate each scene → score to a supplied track or an
  original bed → deliver the clips + an ordered canvas sequence.
- **Local finisher (Claude Code, opt-in):** the signature parts — beat/tempo
  detection, word-level lyric sync, a lookbook + storyboard PDF, and a beat-synced
  **stitched render**. Needs `ffmpeg` + a small Python venv; degrades gracefully to
  the portable tier where those aren't installed.

Video is priced per second and costs far more than stills — the cost gate matters.

## Setup

- **MCP (required):** if the `titles_*` tools are missing, connect first — see `titles-setup`.
- **Local finisher (optional):** `bash scripts/setup.sh .mv-venv` — creates a venv
  (numpy, demucs, faster-whisper, matplotlib, pillow); `ffmpeg` must be on PATH
  (`brew install ffmpeg`). Only needed for the beat/lyric cut, the PDFs, and the
  stitched render. Skip it and the skill still runs MCP-only.

## Phase 0 — Preflight

`titles_get_me` (auth), confirm the account can spend, and settle the track: the user
supplies one, **or** generate an original bed/song with **`generate-music`** (instrumental,
or a full vocal via its `lyrics` input). Decide before generating footage — it drives pacing.

## Phase 1 — Footage (MCP · portable)

1. **Hero + character consistency.** Generate one hero still with `generate-image` (a real
   artist model). Hold the character **scene to scene** by editing that hero into each new
   setting with **`edit-image`** (pixel-locked identity — Nano Banana Pro's `excels_at` lists
   *character-consistency*), rather than re-rolling from scratch. Lighter fallback: reuse one
   `model_id` + a **verbatim character descriptor** in every prompt (see Craft rules).
2. **Review the stills before animating** — stills cost ~10× less than clips. On Claude Code,
   build the lookbook PDF (`build_lookbook_pdf.py`); on MCP-only surfaces, review on the
   canvas. Approve/swap here, not after.
3. **Animate** each approved still (`animate-image`). **Pin one video model + duration +
   aspect** so clips concatenate cleanly. For **clip-to-clip continuity**, use
   **first-&-last-frame** (feed the previous clip's last frame as the start frame → seamless
   motion), or pass the hero as a **reference image** so each clip re-grounds the character.
4. **Optional audio-reactive / SFX:** some video models accept a `background_audio` input
   (animate in time to the track/stem) and a `generate_audio` flag (per-clip foley). Confirm
   support with `titles_resolve_input_constraints`.
5. **Download:** prefer **`titles_download_asset({ output_id, format })`** (short-lived,
   no-auth URL). `scripts/fetch.sh` (adds a `Referer` header for the signed CDN URL) is a
   local-only fallback if you're scripting the pull.

## Phase 2 — Music & lyrics

- **Track:** the user's own, or one from `generate-music`. Because you can author the
  lyrics, timing/scene-mapping is exact.
- **Local finisher:** `analyze_audio.py` (tempo, beat grid, energy/section map) and
  `transcribe.py --isolate` (Demucs vocal stem → word-level timestamps → `lyrics.json`).
  If the user already has the lyrics, use those; transcription is for the timings. Chant /
  abstract lyrics map to a **theme-world**, not line-by-line.

## Phase 3 — Assemble

- **Portable:** hand back the animated clips + an **ordered canvas sequence** (reuse one
  `session_id`) for the user to finish in an editor.
- **Local finisher:** `assemble.py edit.json` cuts to the grid (motion-onset trim, downbeat
  phase, favor-the-beat durations, stretch-only-when-forced), muxes the track, and writes
  `edl.json`. Output aspect is configurable (`out_w/out_h/fit` → 9:16); clip lengths auto-probed.

## Phase 4 — Review

- **Local:** `build_review_pdf.py edl.json lyrics.json storyboard.pdf` — one row per shot
  (thumbnail · time · scene · lyric). Iterate the cut without regenerating clips.
- **Portable:** the ordered canvas sequence link.

## Continuity techniques

- **Scene → scene (identity):** `edit-image` edit-from-hero (tightest); or one model + a
  verbatim descriptor (cheapest). Nano Banana Pro is the character-consistency workhorse.
- **Clip → clip (motion):** first-&-last-frame chaining (last frame of clip N = first frame
  of clip N+1); or reference-image video to re-ground the character each clip.

## Finishing & extras

`upscale-video` for a crisp final (or `upscale-image` on the hero); `restyle-video` to unify
a look across clips; `generate-image` via a text-strong model for a **title card / lyric
type**; `blend-images` for double-exposure transitions.

## Craft rules

- **Motion can't animate a static pose** — bake the action into the still (riding, leaping,
  mid-splash), then prompt the motion that continues it.
- **Character lock = one model + a verbatim descriptor** (or `edit-image` from a hero).
- **Pick the model by its tags** (`subjects` / `excels_at` / `style`); flux for busy scenes,
  sdxl reads storybook.
- **Distinct clips over reuse** — one clip per shot; if you must reuse, pull a different
  section, and budget for enough clips first.

## Cost

Every execution returns `cost_usd`; a run over the confirmation threshold returns
`price_confirmation_required` unless you pass an approved `max_price_usd`. Surface the clip
count and projected spend before a batch — video dominates the cost.

## Bundled scripts (local finisher)

`setup.sh` · `fetch.sh` · `analyze_audio.py` · `transcribe.py` · `assemble.py` ·
`build_review_pdf.py` · `build_lookbook_pdf.py` · `templates/edit.example.json`. All opt-in;
none run on a pure-MCP surface.
