#!/usr/bin/env python3
"""Validate the titles-skills repo against Claude skill standards.

Run locally:  python3 scripts/validate_skills.py
In CI:        exits 1 on any error, prints GitHub ::error annotations.

This repo is a flat skills directory (installable via `npx skills add
titlesnyc/titles-skills` and, for Claude Code, by pointing at skills/<name>).
Each check below maps to a failure mode that has actually broken skill syncs:

  - skills/ exists and contains ONLY skill directories — a loose file (a stray
    .zip especially) silently breaks claude.ai sync for the whole set
  - every skill dir has a SKILL.md with YAML frontmatter
  - frontmatter has name: (required — claude.ai zip upload has no directory
    fallback) and description:, and name matches the directory name
  - description is within Anthropic's hard 1024-character cap (longer =
    truncated, which degrades triggering)
  - no junk tracked anywhere: .DS_Store, *.zip, *.skill
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
errors = []


def err(msg, file=None):
    errors.append(msg)
    print(f"::error {'file=' + str(file) if file else ''}::{msg}")


def frontmatter(path):
    """Return a dict of top-level frontmatter keys, folding block descriptions
    (`>`/`|`) into a single space-joined string, or None if no frontmatter."""
    lines = path.read_text(encoding="utf-8").split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    fm = []
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        fm.append(ln)
    keys, i = {}, 0
    while i < len(fm):
        m = re.match(r"^([A-Za-z0-9_-]+):\s?(.*)$", fm[i])
        if m:
            key, val = m.group(1), m.group(2).strip()
            if key == "description" and val in (">", "|", ">-", "|-", ""):
                block, j = [], i + 1
                while j < len(fm) and (fm[j].startswith((" ", "\t")) or fm[j].strip() == ""):
                    block.append(fm[j].strip())
                    j += 1
                keys["description"] = " ".join(x for x in block if x)
                i = j
                continue
            keys[key] = val
        i += 1
    return keys


if not SKILLS.is_dir():
    err("missing skills/ directory", SKILLS)
else:
    for child in sorted(SKILLS.iterdir()):
        if child.name.startswith("."):  # .gitkeep etc.
            continue
        if not child.is_dir():
            err(f"loose file in skills/: '{child.name}' — skills/ must contain only skill directories", child)
            continue
        skillmd = child / "SKILL.md"
        if not skillmd.exists():
            err(f"skill '{child.name}' has no SKILL.md", child)
            continue
        fm = frontmatter(skillmd)
        if fm is None:
            err(f"{child.name}/SKILL.md has no YAML frontmatter (must start with '---')", skillmd)
            continue
        name = fm.get("name", "").strip("\"'")
        if not name:
            err(f"{child.name}/SKILL.md missing 'name:' (required — claude.ai zip upload has no dir fallback)", skillmd)
        elif name != child.name:
            err(f"{child.name}/SKILL.md name '{name}' != directory '{child.name}'", skillmd)
        desc = fm.get("description", "")
        if not desc:
            err(f"{child.name}/SKILL.md missing 'description:'", skillmd)
        elif len(desc) > 1024:
            err(f"{child.name}/SKILL.md description is {len(desc)} chars — over Anthropic's 1024 cap", skillmd)

for p in ROOT.rglob("*"):
    if ".git/" in str(p) or p.is_dir():
        continue
    if p.name == ".DS_Store" or p.suffix in (".zip", ".skill"):
        err(f"junk file tracked: {p.relative_to(ROOT)} (add to .gitignore; never commit zips/.DS_Store)", p)

print(f"\nvalidate_skills: {len(errors)} error(s)")
sys.exit(1 if errors else 0)
