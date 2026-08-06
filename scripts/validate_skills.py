#!/usr/bin/env python3
"""Validate the titles-skills marketplace against Claude plugin/skill standards.

Run locally:  python3 scripts/validate_skills.py
In CI:        exits 1 on any error, prints GitHub ::error annotations.

Layout: marketplace-root plugin (`"source": "./"`), so `skills/` sits at the repo
root rather than under a plugin subdirectory:

    .claude-plugin/marketplace.json      # lists every plugin
    .claude-plugin/plugin.json           # manifest for the root plugin
    skills/<skill-name>/SKILL.md

A plugin subdirectory (`<plugin>/.claude-plugin/plugin.json` +
`<plugin>/skills/`) is still supported for any entry whose `source` is not the
repo root, so both shapes validate.

The root `skills/` layout is deliberate: it is also the default path a Hermes
skill tap probes (`hermes skills tap add titlesnyc/titles-skills`), and the
Hermes CLI offers no way to override that path. Moving `skills/` back under a
plugin subdirectory silently yields an empty tap.

Each check maps to a failure mode that has actually broken skill syncs:
  - marketplace.json + every plugin.json are valid JSON with required fields
  - every marketplace plugin entry resolves to a dir whose plugin.json name matches
  - every plugin dir on disk is listed in marketplace.json
  - skills/ contains ONLY skill directories (a stray file — a .zip especially —
    silently breaks the whole plugin's claude.ai sync)
  - every skill dir has a SKILL.md with YAML frontmatter
  - frontmatter has name: (required — claude.ai zip upload has no directory
    fallback) and description:, and name matches the directory
  - description stays within Anthropic's hard 1024-character cap
  - no invisible unicode anywhere in a SKILL.md — Hermes's skill scanner scores
    zero-width/bidi characters `high`, and at community trust one high finding
    blocks `hermes skills install` outright (no --force override for a repo we
    don't control the trust level of)
  - no junk tracked anywhere: .DS_Store, *.zip, *.skill
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
errors, warnings = [], []


def err(msg, file=None):
    errors.append(msg)
    print(f"::error {'file=' + str(file) if file else ''}::{msg}")


def warn(msg, file=None):
    warnings.append(msg)
    print(f"::warning {'file=' + str(file) if file else ''}::{msg}")


def frontmatter(path):
    """Top-level frontmatter keys -> value; block descriptions (>/|) folded to a
    single space-joined string so length can be checked. None if no frontmatter."""
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


# --- marketplace.json ---
mkt_path = ROOT / ".claude-plugin" / "marketplace.json"
mkt = None
if not mkt_path.exists():
    err("missing .claude-plugin/marketplace.json", mkt_path)
else:
    try:
        mkt = json.loads(mkt_path.read_text())
    except json.JSONDecodeError as e:
        err(f"marketplace.json is not valid JSON: {e}", mkt_path)
    if mkt is not None:
        for k in ("name", "owner", "plugins"):
            if k not in mkt:
                err(f"marketplace.json missing required key '{k}'", mkt_path)

def local_source_dir(source):
    """Resolve an entry's `source` to a repo-relative dir, or None if not local.

    `"./"` (or `"."`) means the marketplace root is itself the plugin root, so it
    resolves to "" — the repo root. A dict source (github/npm/git) is remote and
    has nothing on disk to validate.
    """
    if not isinstance(source, str):
        return None
    s = source.strip()
    if s in ("", ".", "./"):
        return ""
    return s.lstrip("./")


listed = {}
plugin_roots = {}   # plugin name -> plugin root dir on disk
if mkt and isinstance(mkt.get("plugins"), list):
    for entry in mkt["plugins"]:
        name = entry.get("name")
        if not name:
            err(f"marketplace plugin entry missing name: {entry}", mkt_path)
            continue
        if "source" not in entry:
            err(f"marketplace plugin entry '{name}' missing source", mkt_path)
            continue
        listed[name] = entry
        src = local_source_dir(entry.get("source"))
        if src is None:
            continue   # remote source — nothing on disk to check
        pdir = ROOT / src if src else ROOT
        plugin_roots[name] = pdir
        pj = pdir / ".claude-plugin" / "plugin.json"
        if not pj.exists():
            if entry.get("strict") is False:
                continue   # strict:false — the marketplace entry is the whole definition
            rel = f"{src}/" if src else ""
            err(f"plugin '{name}': no plugin.json at {rel}.claude-plugin/plugin.json "
                f"(add one, or set \"strict\": false on the entry)", mkt_path)
            continue
        try:
            pjson = json.loads(pj.read_text())
        except json.JSONDecodeError as e:
            err(f"plugin '{name}': plugin.json invalid JSON: {e}", pj)
            continue
        if pjson.get("name") != name:
            err(f"plugin '{name}': plugin.json name '{pjson.get('name')}' != marketplace entry", pj)
        if pjson.get("version") != entry.get("version"):
            warn(f"plugin '{name}': version mismatch — plugin.json {pjson.get('version')} vs marketplace {entry.get('version')}", pj)

# --- plugin dirs on disk that nothing lists ---
for pj in ROOT.glob("*/.claude-plugin/plugin.json"):
    pdir = pj.parent.parent
    try:
        pname = json.loads(pj.read_text()).get("name")
    except json.JSONDecodeError:
        continue
    if pname not in listed:
        warn(f"plugin dir '{pdir.name}' (name '{pname}') not listed in marketplace.json", pj)

# --- per-skill checks, for every plugin root the marketplace points at ---
# Zero-width and bidi characters: Hermes's scanner scores these `high`, and one
# high finding blocks install at community trust. Invisible by definition, so a
# human review will not catch them — see tools/skills_guard.py::INVISIBLE_CHARS.
INVISIBLE = {
    "​", "‌", "‍", "⁠", "⁢", "⁣", "⁤",
    "﻿", "‪", "‫", "‬", "‭", "‮",
}

for pname, pdir in sorted(plugin_roots.items()):
    skills = pdir / "skills"
    if not skills.is_dir():
        err(f"plugin '{pname}': no skills/ directory at {skills.relative_to(ROOT)}/", skills)
        continue
    for child in sorted(skills.iterdir()):
        if child.name.startswith("."):
            continue
        label = child.relative_to(ROOT)
        if not child.is_dir():
            err(f"loose file in {skills.relative_to(ROOT)}/: '{child.name}' — skills/ must contain only skill directories", child)
            continue
        skillmd = child / "SKILL.md"
        if not skillmd.exists():
            err(f"skill '{label}' has no SKILL.md", child)
            continue
        fm = frontmatter(skillmd)
        if fm is None:
            err(f"{label}/SKILL.md has no YAML frontmatter (must start with '---')", skillmd)
            continue
        name = fm.get("name", "").strip("\"'")
        if not name:
            err(f"{label}/SKILL.md missing 'name:' (required — claude.ai zip upload has no dir fallback)", skillmd)
        elif name != child.name:
            err(f"{label}/SKILL.md name '{name}' != directory '{child.name}'", skillmd)
        desc = fm.get("description", "")
        if not desc:
            err(f"{label}/SKILL.md missing 'description:'", skillmd)
        elif len(desc) > 1024:
            err(f"{label}/SKILL.md description is {len(desc)} chars — over Anthropic's 1024 cap", skillmd)
        for n, line in enumerate(skillmd.read_text(encoding="utf-8").split("\n"), start=1):
            bad = sorted({f"U+{ord(ch):04X}" for ch in line if ch in INVISIBLE})
            if bad:
                err(f"{label}/SKILL.md:{n} invisible unicode ({', '.join(bad)}) — "
                    f"Hermes scores this 'high' and blocks install at community trust", skillmd)

# --- repo-wide junk ---
for p in ROOT.rglob("*"):
    if ".git/" in str(p) or p.is_dir():
        continue
    if p.name == ".DS_Store" or p.suffix in (".zip", ".skill"):
        err(f"junk file tracked: {p.relative_to(ROOT)} (add to .gitignore; never commit zips/.DS_Store)", p)

print(f"\nvalidate_skills: {len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
