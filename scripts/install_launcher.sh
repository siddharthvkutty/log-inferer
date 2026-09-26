#!/usr/bin/env bash
# Installs a .desktop launcher pointing at this checkout, so Log Inferer shows
# up in your application menu. Uses absolute paths in the .desktop file itself
# (Exec=/Path=), so no PATH/.bashrc changes are needed.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
APPS_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$APPS_DIR/log-inferer.desktop"

mkdir -p "$APPS_DIR"
chmod +x "$PROJECT_DIR/run.sh"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Log Inferer
Comment=Diagnose error logs locally with Ollama
Exec=$PROJECT_DIR/run.sh
Path=$PROJECT_DIR
Icon=$PROJECT_DIR/icon.png
Terminal=false
Categories=Utility;Development;
EOF

command -v update-desktop-database >/dev/null 2>&1 && \
    update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true

echo "Installed: $DESKTOP_FILE"
echo "Log Inferer should now appear in your application menu."
