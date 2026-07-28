---
name: upload-image
description: |
  Bring an outside image into TITLES (titles.xyz) so it can be edited,
  upscaled, blended, restyled, or animated. Use when the user has an image
  that isn't on TITLES yet: "upload this image", "use my own photo", "import
  this picture", "edit this image from a link", "bring this into TITLES",
  "start from this reference". Takes a public image URL (jpeg/png/webp under
  20MB), imports it server-side, and returns an `output_id` the transform
  skills can use. Runs on the TITLES MCP — if TITLES tools are missing,
  connect mcp.titles.xyz/mcp first (see titles-setup). NOT for: images already
  on TITLES (use their `output_id` directly), or generating a new image
  (generate-image).
---

# upload-image

Import an external image into TITLES so the transform skills can work on it. This is the only way to bring an outside image in through the MCP.

> Rolling out — `titles_create_upload` is on staging first. If it isn't in the tool list on this connection, tell the user upload isn't available here yet and that they can add the image directly in the TITLES studio.

## Get connected

Check the tool list for TITLES tools (names contain `titles_`). If missing, hand off to the **titles-setup** skill and stop.

## 1. Get a public URL

The tool needs a **public** image URL — jpeg/png/webp, under 20MB, fetchable with no cookies or auth (a hosted image, a CDN link, a file host).

- **Local file:** not supported via MCP yet. Say so plainly — do **not** tunnel a local file or spin up a temp server to fake a public URL. Tell the user to add it in the studio instead.
- **Already on TITLES:** don't re-upload; use its existing `output_id`.

## 2. Import

Call `titles_create_upload({ url, session_id?, title? })`. The backend fetches and imports it and returns the finished `output_id`, `session_url`, and an inline thumbnail. Uploads are **moderated** — a rejected image returns an error and nothing is stored; relay that honestly.

Pass a `session_id` when the upload feeds work already on a canvas, so the import and the generations that consume it stay together.

## 3. Hand off

The returned `output_id` is now a first-class TITLES image. Offer the next step and pass the id straight into it:
- restyle it (**restyle-image**), change one thing (**edit-image**), sharpen it (**upscale-image**), animate it (**animate-image**), or blend it with another (**blend-images**).

## Etiquette

This is an on-ramp, not a destination — confirm the import, show the thumbnail, and move to what the user actually wants to make with it.
