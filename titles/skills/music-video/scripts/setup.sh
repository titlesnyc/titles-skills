#!/usr/bin/env bash
# One-time local tooling for the music-video pipeline (audio analysis, vocal
# isolation, transcription, PDF). Creates a venv so nothing touches system python.
# Usage: bash setup.sh [venv_dir]   (default: .mv-venv in cwd)
set -euo pipefail
DIR="${1:-.mv-venv}"
python3 -m venv "$DIR"
"$DIR/bin/pip" install -q --disable-pip-version-check \
  numpy demucs faster-whisper soundfile matplotlib pillow
echo "venv ready: $DIR   (ffmpeg must also be on PATH: $(command -v ffmpeg || echo MISSING))"
