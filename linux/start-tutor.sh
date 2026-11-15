#!/bin/sh
# Opens a Zulu 1 tutor in its own browser window.
# Usage: start-tutor.sh shakai   or   start-tutor.sh bubba
DIR="$(cd "$(dirname "$0")" && pwd)"
PAGE="$DIR/${1:-shakai}/index.html"
for b in google-chrome google-chrome-stable chromium chromium-browser microsoft-edge brave-browser; do
  if command -v "$b" >/dev/null 2>&1; then exec "$b" --app="file://$PAGE" --window-size=1100,850; fi
done
# No Chrome-type browser: use the default browser (Firefox works too).
exec xdg-open "$PAGE"
