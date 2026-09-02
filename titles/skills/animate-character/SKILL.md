---
name: animate-character
user-invocable: true
argument-hint: [the shots you want]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Carry a character across video shots on TITLES (titles.xyz) and keep them
  recognizable in every clip — animate a locked character from their reference
  sheet, hold face, wardrobe and lighting across a multi-shot sequence, and chain
  shots so they cut together. Use when the user says: "animate my character",
  "put my character in a video", "same character across shots", "a scene with my
  character", "multi-shot sequence", "make my character move", "a short film with
  this character", "keep the character consistent in video". Starts from a
  character sheet (build one with create-character first). Video is priced per
  second, so shots are quoted for approval before anything runs. Runs on the
  TITLES MCP — if TITLES tools are missing, connect mcp.titles.xyz/mcp first (see
  titles-setup). NOT for: one clip from one still with no identity to hold
  (animate-image), a video from text alone (generate-video), style loops from an
  artist's stills (motion-pack), or still images (create-character).
---

# animate-character

Take a character who already exists as images and put them in motion across shots — the same face, wardrobe and world in every clip.

The one rule everything else hangs off: **never ask a video model to invent your character and animate them in the same breath.** A text-to-video model re-casts the role on every run — "a man in a grey sweater" matches thousands of people and it picks one at random each time. Identity has to arrive as a *picture*. Removing that image anchor is measurably catastrophic, not merely worse.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## 1. Start from a locked character

You need reference images of the character before any video. Get them in this order of preference:

- **A character sheet** — anchor + ¾ + side (+ wardrobe views). Ideal: multiple angles means the model can hold the face when the shot turns.
- **A single strong still** of them — workable for one or two shots.
- **Nothing yet** → hand off to **create-character** and stop. Building the sheet in stills costs cents; discovering the character doesn't work *after* paying per-second for video is the expensive way to learn it.

Also carry over the **Character Anchor** text (the frozen identity description) if they have one — you won't put it in most prompts, but you need it to judge drift in step 5.

## 2. Plan the shots, then pin the set

Get the shot list from the user — what happens, where, how many clips. Then **pin these once, for the whole sequence**, and say them back:

| Pin | Why |
|---|---|
| **model** | Different architectures have different grain, color and skin rendering. Switching mid-sequence looks like a different production. |
| **aspect ratio** | Clips at different ratios can't cut together without reframing. |
| **resolution** | Mixing 1080p and 720p shows at every cut. |
| **duration** | Keeps pacing even and makes one probe clip a valid cost estimate for the rest. |
| **lighting / time of day** | A warm-lit shot cut against a cool-lit one reads as a different location — and shifted shadows can change the face. |
| **wardrobe** | Clothing drifts faster than faces. Fix it in the refs *and* keep it in the pin. |

If you let the model pick these per clip, you don't get a scene — you get a montage of unrelated footage. Move lighting and time-of-day **incrementally** across a sequence rather than cutting between extremes.

**Keep clips short.** Ask for **4–8 seconds** and treat ~10s as the ceiling even when the model allows more: first-frame conditioning weakens as clips get longer, and long single-pass renders degrade. A longer beat is several chained short clips (step 6), never one long generation.

## 3. Pick the video model — and offer the tiers

Resolve live with `titles_search_models({ operator: "imgRefs2VidNode" })` for the reference-guided path and look for continuity tags (`reference-guided-subject-continuity-prototyping`, `multi-shot-short-form-narrative`, `reference-guided-character-and-product-previsualization`). Then read the real limits for your pick — the reference cap, the allowed `duration` / `resolution` / `aspect_ratio` values, and whether audio is supported:

```
titles_resolve_input_constraints({ operator_id: "imgRefs2VidNode", adapter_id: <from the search result> })
```

Roughly, at time of writing — verify rather than trusting these:

- **Seedance 2.0** — the multi-shot continuity workhorse; ~9 image refs, up to 4K.
- **Seedance 2.0 Fast** — same ~9 refs, capped at 720p, cheaper. **Identity capability is not what you give up** — only resolution — so this is the honest default for previs and drafts.
- **Veo 3.1 / 3.1 Fast** — fewer refs, but native audio and strong first-to-last-frame transitions. Flat per-second pricing, and **audio roughly doubles it**.

Quote from a **live** `cost_usd`, never from a model's advertised rate — the real charge includes the platform fee. Video is per-second, so give the user the arithmetic: *"at $X for a 5-second clip, your 6 shots run about $Y."* Then let them pick a tier.

## 4. Generate shot by shot

**One clip per call** (these operators cap `outputs_count` at 1), sequentially, on one shared `session_id`.

**Reference-guided — the identity path.** Pass the character sheet as refs:

```
titles_run_execution({
  operator_id: "imgRefs2VidNode",
  inputs: {
    image: [{ output_id: <anchor> }, { output_id: <¾> }, ...],   // the sheet
    model: { model_id, adapter_id },
    prompt: <the motion + the setting>,
    duration, resolution, aspect_ratio, generate_audio
  },
  outputs_count: 1,
  session_id
})
```

**Animating one exact frame instead.** If a specific still *is* the shot's first frame, `titles_animate_image({ output_id, prompt, duration?, model_id?, session_id })` is the simpler call. For a controlled A→B move — a character crossing to a known end pose — pass `end_output_id` as well and the clip lands exactly on that frame.

### Prompt the motion, not the character

**This is the opposite of the stills rule, and getting it backwards is the most common mistake here.** In `create-character` you repeat the identity block verbatim in every prompt. In image-to-video you **don't** — the first frame already carries the face, the hair, the wardrobe. Re-describing them invites the model to split the difference between what it *sees* and what it *reads*, and satisfy neither.

So the prompt is the movement: *"slow dolly-in as she lowers the cup and looks off-camera."* Not the person.

Two exceptions, both narrow:
- **Reference-guided multi-ref calls** (`imgRefs2VidNode`) take a scene as well as motion, and benefit from the same **negation** the stills skill uses: *"use these references for identity only — do not copy their backgrounds, framing or lighting."*
- **A partial or ambiguous ref** (a face-only still driving a full-body shot) needs the missing parts described — wardrobe, build — word-for-word the same in every clip that needs it.

**Keep the motion moderate.** Walking, a turn of the head, a slow push-in. Fast spins, whip pans, and head turns past about 45° are where faces warp and smear. If the story needs a big move, build it across shorter clips instead of asking one clip to do it.

Video clears the confirmation threshold, so expect **`price_confirmation_required`** on the first call — that's a quote, nothing has run or charged. Relay the exact `cost_usd`, get approval, then re-call with `max_price_usd` set to the approved amount. Never set it unprompted.

Renders are slow: expect several `titles_await_execution` re-entries per clip.

## 5. Check every clip as it lands — and offer a re-render

**After each clip, not at the end of the sequence** — video is the most expensive thing on the platform and a wrong pin found at clip 1 saves the whole budget. `titles_get_execution` inlines a preview frame; look at it and grade two independent axes:

**A. Did identity hold?** Against the sheet: face (jaw, nose, eye spacing) → hair → **wardrobe, which drifts fastest because models prioritize faces** → age and skin tone → distinguishing marks, on the correct side.

**B. Did it do what you asked?** The motion, the framing, the pacing — separately from the likeness. Watch specifically for: identity morphing partway through the clip, face warping on the largest movement, and a near-frozen tail where the motion decelerates.

Then **say what you see and offer the re-render with its price** — never quietly accept a bad clip, and never quietly retry one either:

> "Clip 3 holds the face but her jacket shifted from charcoal to black, and the last half-second is nearly frozen. Re-render at $X, accept it, or move on?"

Re-render **from the sheet or the intended first frame — never from the flawed clip's last frame**. Change one thing. Cap it at two attempts per shot, then stop and offer to drop the shot, accept the closest take, or change the pin. Whether a soft miss is worth another per-second charge is the user's call, not yours.

## 6. Chain shots so they cut together

For a continuous beat, take the **last frame of clip N as the first frame of clip N+1** — that carries pose *and* lighting state forward, which is what makes a cut work.

Two things make or break it:

- **Never feed a dirty frame forward.** If the final frame is noisy, blurred or mid-artifact, clean it (`titles_upscale_image`) or pick a cleaner frame first. Chaining a degraded frame compounds the degradation, and color creeps warmer or cooler across a long chain.
- **Trim the deceleration tail.** Generated clips slow to a stop at the end; joining on those near-static frames reads as a freeze at the seam. Cut on live motion.

Re-anchor to the original sheet every few shots rather than chaining indefinitely — each hop is a fresh chance for the face to move.

## 7. Deliver + hand off

- The `session_url` (canvas) — raw output URLs 403.
- Each clip via `titles_download_asset({ output_id, format: "mp4" })` — host-adaptive: `curl` to disk on a shell host (Claude Code / Codex), a short-lived link on a chat host.
- **Write down the sequence:** the pinned model / aspect / resolution / duration, the sheet `output_id`s used, and the clips in shot order. That's what makes an extra shot next week match the ones from today.
- Say plainly that **stitching, trimming and grading happen outside TITLES** — the platform returns individual clips, not an edit. Offer the trim/seam notes from step 6 so whoever cuts it knows where the joins are.
- Offer next steps: sharpen a hero clip (**upscale-video**), change a clip's look (**restyle-video**), or publish with the artist credited (`titles_publish`).

## Honest limits

Say these before spending, not after:

- **Two characters in a close-up blur together.** No current platform holds two identities in tight interaction — TITLES included. Keep characters in separate shots, or shoot them apart in frame.
- **There's no seed.** You cannot re-roll the identical take; reference anchoring is the reproducibility mechanism, and it gets you close, not exact.
- **Consistency and motion pull against each other.** The conditioning that holds a face also damps how much it can move. A very dynamic shot and a perfectly held face are competing requests — say which one the shot needs.
- **Long clips degrade.** Past roughly 10 seconds, first-frame conditioning fades and drift accelerates; a minute in one pass is not a thing. Sequences are built from short clips.
- **No audio bed.** Video models can generate a clip's own sound, but a soundtrack across the sequence isn't part of this — `generate-music` and `text-to-speech` make tracks separately, and they're laid in during the edit.

## Etiquette

Refuse to text-to-video a character; send them to build a sheet first. Pin the set before the first clip and say what's pinned. Quote per-second cost with real arithmetic, gate the first clip as a calibration, check each clip as it lands, and hand back a sequence whose pins are written down so tomorrow's shot matches today's.

