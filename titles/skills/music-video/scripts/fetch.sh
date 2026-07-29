#!/usr/bin/env bash
# Download a TITLES output asset. The signed CDN URL (from titles_get_output ->
# output.asset.url) is hotlink-protected: a bare GET 403s. A Referer header fixes it.
# Usage: bash fetch.sh <signed_cdn_url> <out_path>
set -euo pipefail
curl -fsS -H "Referer: https://www.titles.xyz/" -o "$2" "$1"
echo "saved $2 ($(stat -f%z "$2" 2>/dev/null || stat -c%s "$2") bytes)"
