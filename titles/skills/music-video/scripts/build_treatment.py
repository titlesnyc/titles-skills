"""Treatment scaffold — turn song understanding into a beat sheet BEFORE any
footage is generated. Reads analysis.json (sections + tempo, from analyze_audio.py)
and lyrics.json (word/line timings, from transcribe.py) and emits a beat sheet:
one row per song section, its timecode, energy level, and the lyric over it — with
blank Scene + Motif columns for the agent (or user) to fill in. That filled sheet is
the plan Phase "Footage" generates against, and the precursor to edit.json.

Usage: python build_treatment.py analysis.json lyrics.json treatment.md ["Title"]
Pass "" for lyrics.json to scaffold from structure alone (instrumental).
"""
import sys, os, json

analysis = json.load(open(sys.argv[1]))
lyr = (json.load(open(sys.argv[2]))["lines"]
       if len(sys.argv) > 2 and sys.argv[2] and os.path.exists(sys.argv[2]) else [])
out = sys.argv[3] if len(sys.argv) > 3 else "treatment.md"
title = sys.argv[4] if len(sys.argv) > 4 else "Untitled"

secs = analysis.get("sections", [])
dur = analysis.get("duration", 0)
bpm = analysis.get("bpm")

def fmt(t):
    m, s = divmod(int(round(t)), 60)
    return f"{m}:{s:02d}"

rows = []
for i, s in enumerate(secs):
    a, b = s["start"], s["end"]
    over = [l["text"] for l in lyr if l["start"] < b - 0.05 and l["end"] > a + 0.05]
    rows.append({
        "section": i + 1,
        "start": round(a, 2), "end": round(b, 2),
        "range": f"{fmt(a)}–{fmt(b)}",
        "level": s.get("level", ""),
        "lyric": " / ".join(over) if over else "(instrumental)",
        "scene": "", "motif": "",
    })

md = [
    f"# {title} — treatment (beat sheet)",
    "",
    f"- duration **{fmt(dur)}** ({dur:.1f}s) · tempo **~{bpm} BPM**",
    f"- {len(secs)} sections · energy arc = the emotional shape (hold in the quiet, cut fast at the peaks)",
    "",
    "Fill **Scene** (what illustrates this section) and **Motif** (the recurring hero/",
    "image that returns on the hook). Generate footage to this sheet — don't retrofit a",
    "story onto random clips. Then translate rows → `edit.json` shots.",
    "",
    "| # | time | energy | lyric / section | Scene (fill) | Motif (fill) |",
    "|---|---|---|---|---|---|",
]
for r in rows:
    md.append(f"| {r['section']} | {r['range']} | {r['level']} | {r['lyric']} |  |  |")
open(out, "w").write("\n".join(md) + "\n")
json.dump({"title": title, "duration": dur, "bpm": bpm, "rows": rows},
          open(os.path.splitext(out)[0] + ".json", "w"), indent=1)
print(f"treatment: {out}  ({len(rows)} sections)  + {os.path.splitext(out)[0]}.json")
