---
name: create-character
user-invocable: true
argument-hint: [who the character is]
# allowed-tools omitted by design — the titles_* MCP prefix varies by connection (mcp__titles__ / mcp__titles-staging__ / a claude.ai connector), so pinning tools would break portability
description: >
  Create a reusable character on TITLES (titles.xyz) and hold them consistent
  across images — write the identity spec, lock a master anchor portrait, build a
  multi-angle character sheet, then generate scenes that keep the same face,
  wardrobe, and details. Use when the user says: "create a character",
  "consistent character", "the same person in every image", "character sheet",
  "keep this character consistent", "character design", "a mascot for my brand",
  "my protagonist", "turnaround sheet", "different poses of this character".
  Hands back a reusable set of reference `output_id`s any other TITLES skill can
  take. Runs on the TITLES MCP — if TITLES tools are missing, connect
  mcp.titles.xyz/mcp first (see titles-setup). NOT for: a one-off image with no
  reuse (generate-image), restyling an existing image (restyle-image), one
  targeted edit (edit-image), or surveying artist styles (style-explorer).
---

# create-character

Build a character once, then reuse them. Identity comes from **reference images**, style comes from an **artist model**, and the scene is the only thing that changes per shot.

TITLES has no character *training* — identity is held by conditioning on reference images. That's a strength here, not a workaround: the reference caps are big enough to carry a whole character sheet (Nano Banana Pro takes **up to 14** reference images), and there's no dataset to curate, no training fee, and no wait. Verify the live cap for your chosen model with `titles_resolve_input_constraints({ operator_id: "imgEditNode", adapter_id })` rather than assuming this number.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop — never fall back to a non-TITLES tool.

## 1. Write the character spec — ask, never invent

The character is the **user's** to define. If you don't have it, ask and stop; don't invent a person from a category name ("a mascot" is not a character).

Get as many of these as they'll give, and write them down as one block — this becomes the **Character Anchor**:

- age · gender presentation · ethnicity / skin tone · build
- hair: color, texture, length, style
- eyes: color, shape
- distinguishing marks: scars, tattoos, freckles, glasses, piercings — **with side/placement** ("cybernetic eye on the left")
- signature wardrobe, in exact color words ("scarlet wool double-breasted coat", not "red coat")

Then hold three rules for the rest of the session:

- **Freeze the wording.** Copy the Anchor in verbatim every time. Swapping a synonym — "auburn" for "copper" — is the single most common cause of a face changing between shots.
- **Identity before style.** Put physical traits ahead of style/mood words in the prompt; long style phrasing pushes identity tokens down and they lose weight.
- **Fine detail needs a picture, not a sentence.** Freckles, tattoos, logos and text on clothing do not survive on words alone — they hold because they're in the reference images from step 3 onward. Say so rather than promising them from prompt text.

## 2. Pick the style layer (artist model)

Identity and style are separate jobs. The artist model decides *how it's rendered*; the Anchor decides *who it is*. Keeping them apart is what stops a style change from being misread as the character drifting.

`titles_search_models({ operator: "txt2ImgNode" })` on the look the user wants, pick the best fit, name the artist and credit them with their `model_url`. **Use this one model for the whole character** — switching mid-set changes the rendering and reads as a different character.

## 3. Lock the master anchor portrait

One image, and everything later descends from it:

- **Clean and legible, not dramatic.** Front-facing, both eyes visible, even light, plain background, no heavy shadow. Clarity beats mood here — artifacts in the anchor get amplified into every later generation.
- `titles_generate_image({ prompt: <Anchor + "front-facing portrait, neutral background, even lighting">, model_id, aspect_ratio: "1:1" })`. Submit directly (stills are cheap) and report `cost_usd`.
- Look at the result (`titles_get_execution` inlines previews) and check it against the spec before going on. Regenerate now if it's off — everything downstream inherits this frame.
- Show it to the user and get a yes. This is the cheapest possible place to change direction.

**Outside photo instead?** If they want their own reference, bring it in with `titles_create_upload({ url })` (public jpeg/png/webp URL) and use that as the anchor. Local files aren't supported via MCP — say so plainly rather than improvising a host.

## 4. Build the character sheet

Now make the extra views, each generated **from the anchor** with `titles_edit_image` — the anchor as the reference image, the prompt describing only the new angle or state:

- **Angles: ¾, side, back.** This is the step most people skip and it's why profiles break — reference conditioning is trained mostly on front-facing faces, so without these views a side or rear shot invents a new face.
- **Expressions:** neutral, a smile, a serious beat. Keep them mild — extreme expressions distort face geometry and confuse later conditioning.
- **Wardrobe/state variants** only if the story needs them.

Use a model that's good at identity — `titles_search_models({ query: "nano banana", operator: "imgEditNode" })` (Nano Banana Pro self-tags `character-consistency`). **Quote the sheet as a batch before running it** — per-image cost × number of views, one total, get a go.

The finished sheet is the deliverable of this phase: a set of `output_id`s that *is* the character. Keep the list; step 5 and every later session feed from it.

## 5. Generate scenes — always from the sheet

For each scene, pass the sheet as reference images and let the prompt carry only what changes:

```
titles_edit_image({
  output_id: [<anchor>, <¾>, <side>, ...],   // the sheet — an ARRAY of refs
  prompt: <role assignment> + <Character Anchor, verbatim> + <the scene>,
  model_id: <identity model from step 4>,
  session_id
})
```

Two rules do most of the work:

- **Never generate a scene from the previous scene's output.** Always go back to the anchor/sheet. Chaining compounds drift — every hop is a fresh chance for the face to move.
- **Assign roles to the references explicitly.** Multi-reference models do **not** infer what each image is for. Say it: "use image 1 for the face and hair, image 2 for the outfit, keep the character from these references and place them in ⟨scene⟩." Unlabeled refs bleed pose, lighting and background from whichever image the model latches onto.

Cap the number of refs at the model's resolved limit, and lead with the anchor.

## 6. Check for drift before you deliver

Look at every result next to the anchor (`titles_get_execution` inlines previews) and check, in this order — these are the things that actually fail:

1. **face** — jaw width, nose, eye spacing, hairline
2. **hair** — color and style, not just length
3. **wardrobe** — color and cut; this drifts faster than the face because models prioritize faces
4. **age and skin tone** — both drift toward whatever the scene context implies
5. **distinguishing marks** — present, and on the correct side

Name what drifted instead of quietly shipping it. The fix is almost always: regenerate from the anchor (never from the drifted output), add the missing angle to the sheet, or restate the Anchor verbatim where the wording slipped.

## 7. Deliver + hand off the character

- The `session_url` (canvas) — raw output URLs 403.
- Files via `titles_download_asset({ output_id, format: "png" })` — host-adaptive: `curl` to disk on a shell host (Claude Code / Codex), a short-lived link on a chat host.
- **Write the character down** so it survives the session: the frozen Character Anchor text, the artist `model_id` + artist credit, and the sheet's `output_id`s in order with what each view is. That list is the reusable character — it's what makes the next session cheap.
- Offer the next step and pass the sheet along: put them in a campaign (`promo-pack`), animate them (`animate-image`, or `imgRefs2VidNode` via `titles_run_execution` for reference-guided video), or publish with credit (`titles_publish`).

## Honest limits

Say these up front rather than letting the user discover them:

- **Two characters in a close-up blur into each other.** No current platform holds two identities in tight interaction — TITLES included. Keep characters in separate shots, or accept the risk.
- **There's no seed to lock.** Reference anchoring *is* the reproducibility mechanism here; identical re-runs aren't available, and seeds never held identity anyway (they hold composition).
- **Reference conditioning is very good, not perfect.** Expect a strong likeness, not a forensic match — the last few percent of fine detail is what trained-model approaches buy elsewhere.

## Etiquette

Ask for the character, never invent one. Gate at the anchor (cheap) rather than after a full set (not cheap). Quote batches before running them, report the running cost, credit the artist, and hand back a character the user can reuse tomorrow.

