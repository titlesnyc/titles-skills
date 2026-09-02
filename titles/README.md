# titles

titles.xyz creative tools on the **TITLES MCP** (`mcp.titles.xyz/mcp`). Each skill
wraps one creative intent so an agent can drive the TITLES tools correctly on a
user's behalf — finding the right artist-trained model, handling cost
confirmation, and delivering both a canvas link and a downloadable file.

New here? Start with **`titles-setup`** — every other skill hands off to it when
the TITLES tools aren't connected yet.

## Skills

### Images
| Skill | Job |
|---|---|
| `generate-image` | Text → image, in a real artist's style (artist credited + paid) |
| `restyle-image` | Reinterpret a whole image in a new style, keeping its subject |
| `edit-image` | Change one thing, keep the rest |
| `upscale-image` | Bigger and sharper |
| `vary-image` | Fresh takes on an image — no prompt, no model to pick |
| `blend-images` | Merge two images on a balance dial |

### Video
| Skill | Job |
|---|---|
| `generate-video` | Text → a short video clip |
| `animate-image` | Turn a still into a short clip |
| `restyle-video` | Transform an existing clip's look/scene, keeping the motion |
| `upscale-video` | Higher-resolution, sharper video |

### Audio
| Skill | Job |
|---|---|
| `generate-music` | Text → an original music track |
| `text-to-speech` | Text → spoken audio (narration, voiceover) |

### Creative packs
| Skill | Job |
|---|---|
| `create-character` | Build a reusable character + sheet, then hold them consistent across images |
| `animate-character` | Carry a locked character across video shots that cut together |
| `promo-pack` | A full set of promo/campaign assets in one style, sized per channel |
| `motion-pack` | An artist's stills → a set of short motion loops |
| `curation-digest` | Browse the feed, save the best in a style, with a taste report |
| `style-explorer` | Roam the artist library — a wide, varied spread to discover styles |

### Setup
| Skill | Job |
|---|---|
| `titles-setup` | Connect the agent to the TITLES MCP, authenticate, verify |

## About the TITLES MCP

Streamable HTTP + OAuth 2.1 (PKCE + dynamic client registration), so any modern
MCP client connects with no pre-registered credentials.

- **Endpoint:** `https://mcp.titles.xyz/mcp`
- **In-band docs:** once connected, call `titles_help` for the live tool catalog.

Tool behavior is defined by the server; these skills add workflow knowledge on
top (setup, model choice, cost handling, delivery) and never override it. The
model/price catalog is resolved live at runtime — nothing here hardcodes it.
