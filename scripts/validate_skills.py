#!/usr/bin/env python3
"""Validate the titles-skills marketplace against Claude plugin/skill standards.

Run locally:  python3 scripts/validate_skills.py
In CI:        exits 1 on any error, prints GitHub ::error annotations.

Layout (house style — mirrors titlesnyc/titles-internal-skills):

    .claude-plugin/marketplace.json      # lists every plugin
    .agents/plugins/marketplace.json     # Codex mirror of the marketplace
    <plugin>/.claude-plugin/plugin.json  # plugin manifest
    <plugin>/.codex-plugin/plugin.json   # plugin manifest (Codex)
    <plugin>/skills/<skill-name>/SKILL.md

Each check maps to a failure mode that has actually broken skill syncs:
  - marketplace.json + every plugin.json are valid JSON with required fields
  - every marketplace plugin entry resolves to a dir whose plugin.json name matches
  - every plugin dir on disk is listed in marketplace.json
  - the Codex mirror stays in sync: its entries resolve to a .codex-plugin/plugin.json
    whose name matches, every Claude-marketplace plugin appears in it, and the Codex
    plugin.json version tracks the Claude one
  - skills/ contains ONLY skill directories (a stray file — a .zip especially —
    silently breaks the whole plugin's claude.ai sync)
  - every skill dir has a SKILL.md with YAML frontmatter
  - frontmatter has name: (required — claude.ai zip upload has no directory
    fallback) and description:, and name matches the directory
  - description stays within Anthropic's hard 1024-character cap
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


def json_dict(path, label):
    """Parse path as JSON, requiring a top-level object; err + None otherwise."""
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        err(f"{label} is not valid JSON: {e}", path)
        return None
    if not isinstance(data, dict):
        err(f"{label} must be a JSON object, got {type(data).__name__}", path)
        return None
    return data


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
    mkt = json_dict(mkt_path, "marketplace.json")
    if mkt is not None:
        for k in ("name", "owner", "plugins"):
            if k not in mkt:
                err(f"marketplace.json missing required key '{k}'", mkt_path)

listed = {}
if mkt and isinstance(mkt.get("plugins"), list):
    for entry in mkt["plugins"]:
        if not isinstance(entry, dict):
            err(f"marketplace plugin entry must be an object: {entry!r}", mkt_path)
            continue
        name = entry.get("name")
        src = entry.get("source")
        src = src.lstrip("./") if isinstance(src, str) else ""
        if not name or not src:
            err(f"marketplace plugin entry missing name/source: {entry}", mkt_path)
            continue
        listed[name] = entry
        pj = ROOT / src / ".claude-plugin" / "plugin.json"
        if not pj.exists():
            err(f"plugin '{name}': no plugin.json at {src}/.claude-plugin/plugin.json", mkt_path)
            continue
        pjson = json_dict(pj, f"plugin '{name}': plugin.json")
        if pjson is None:
            continue
        if pjson.get("name") != name:
            err(f"plugin '{name}': plugin.json name '{pjson.get('name')}' != marketplace entry", pj)
        if pjson.get("version") != entry.get("version"):
            warn(f"plugin '{name}': version mismatch — plugin.json {pjson.get('version')} vs marketplace {entry.get('version')}", pj)

# --- Codex mirror (.agents/plugins/marketplace.json + <plugin>/.codex-plugin) ---
codex_mkt_path = ROOT / ".agents" / "plugins" / "marketplace.json"
if not codex_mkt_path.exists():
    err("missing .agents/plugins/marketplace.json (Codex marketplace mirror)", codex_mkt_path)
else:
    codex_mkt = json_dict(codex_mkt_path, "Codex marketplace.json")
    if codex_mkt is not None:
        for k in ("name", "plugins"):
            if k not in codex_mkt:
                err(f"Codex marketplace.json missing required key '{k}'", codex_mkt_path)
        codex_listed = set()
        plugins = codex_mkt.get("plugins")
        if plugins is not None and not isinstance(plugins, list):
            err(f"Codex marketplace.json 'plugins' must be a list, got {type(plugins).__name__}", codex_mkt_path)
            plugins = []
        for entry in plugins or []:
            if not isinstance(entry, dict):
                err(f"Codex marketplace plugin entry must be an object: {entry!r}", codex_mkt_path)
                continue
            name = entry.get("name")
            source = entry.get("source")
            src = source.get("path") if isinstance(source, dict) else None
            src = src.lstrip("./") if isinstance(src, str) else ""
            if not name or not src:
                err(f"Codex marketplace plugin entry missing name/source.path: {entry}", codex_mkt_path)
                continue
            codex_listed.add(name)
            cpj = ROOT / src / ".codex-plugin" / "plugin.json"
            if not cpj.exists():
                err(f"Codex plugin '{name}': no plugin.json at {src}/.codex-plugin/plugin.json", codex_mkt_path)
                continue
            cpjson = json_dict(cpj, f"Codex plugin '{name}': plugin.json")
            if cpjson is None:
                continue
            if cpjson.get("name") != name:
                err(f"Codex plugin '{name}': plugin.json name '{cpjson.get('name')}' != marketplace entry", cpj)
            claude_pj = ROOT / src / ".claude-plugin" / "plugin.json"
            if claude_pj.exists():
                # Shape errors on the Claude side are reported by its own loop.
                try:
                    claude_pjson = json.loads(claude_pj.read_text())
                except json.JSONDecodeError:
                    claude_pjson = None
                if isinstance(claude_pjson, dict) and cpjson.get("version") != claude_pjson.get("version"):
                    warn(f"Codex plugin '{name}': version {cpjson.get('version')} != Claude plugin.json {claude_pjson.get('version')}", cpj)
        for name in listed:
            if name not in codex_listed:
                err(f"plugin '{name}' is in the Claude marketplace but missing from the Codex mirror", codex_mkt_path)

# --- every plugin dir on disk listed? + per-skill checks ---
for pj in ROOT.glob("*/.claude-plugin/plugin.json"):
    pdir = pj.parent.parent
    try:
        pdata = json.loads(pj.read_text())
    except json.JSONDecodeError:
        continue
    if not isinstance(pdata, dict):
        continue
    pname = pdata.get("name")
    if pname not in listed:
        warn(f"plugin dir '{pdir.name}' (name '{pname}') not listed in marketplace.json", pj)
    skills = pdir / "skills"
    if not skills.is_dir():
        continue
    for child in sorted(skills.iterdir()):
        if child.name.startswith("."):
            continue
        if not child.is_dir():
            err(f"loose file in {pdir.name}/skills/: '{child.name}' — skills/ must contain only skill directories", child)
            continue
        skillmd = child / "SKILL.md"
        if not skillmd.exists():
            err(f"skill '{pdir.name}/{child.name}' has no SKILL.md", child)
            continue
        fm = frontmatter(skillmd)
        if fm is None:
            err(f"{pdir.name}/{child.name}/SKILL.md has no YAML frontmatter (must start with '---')", skillmd)
            continue
        name = fm.get("name", "").strip("\"'")
        if not name:
            err(f"{pdir.name}/{child.name}/SKILL.md missing 'name:' (required — claude.ai zip upload has no dir fallback)", skillmd)
        elif name != child.name:
            err(f"{pdir.name}/{child.name}/SKILL.md name '{name}' != directory '{child.name}'", skillmd)
        desc = fm.get("description", "")
        if not desc:
            err(f"{pdir.name}/{child.name}/SKILL.md missing 'description:'", skillmd)
        elif len(desc) > 1024:
            err(f"{pdir.name}/{child.name}/SKILL.md description is {len(desc)} chars — over Anthropic's 1024 cap", skillmd)

# --- repo-wide junk ---
for p in ROOT.rglob("*"):
    if ".git/" in str(p) or p.is_dir():
        continue
    if p.name == ".DS_Store" or p.suffix in (".zip", ".skill"):
        err(f"junk file tracked: {p.relative_to(ROOT)} (add to .gitignore; never commit zips/.DS_Store)", p)

print(f"\nvalidate_skills: {len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
