#!/bin/sh
# Adds "Zulu 1 Tutor" and "Zulu 1 Bubba" to the applications menu. Run once: sh install.sh
# Keep this folder where it is afterwards; the menu items open the tutors from here.
DIR="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$DIR/start-tutor.sh"
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPS"
for e in "shakai:Zulu 1 Tutor:Master Shakai" "bubba:Zulu 1 Bubba:Master Bubba"; do
  id="${e%%:*}"; rest="${e#*:}"; name="${rest%%:*}"; who="${rest#*:}"
  cat > "$APPS/zulu1-$id.desktop" <<DESK
[Desktop Entry]
Type=Application
Name=$name
Comment=Talking spelling tutor for $who
Exec="$DIR/start-tutor.sh" $id
Icon=$DIR/icon.png
Terminal=false
Categories=Education;
DESK
  chmod +x "$APPS/zulu1-$id.desktop"
done
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" >/dev/null 2>&1
echo "Done. Look for \"Zulu 1 Tutor\" and \"Zulu 1 Bubba\" in your applications menu."
