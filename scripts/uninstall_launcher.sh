#!/usr/bin/env bash
# Removes the .desktop launcher installed by install_launcher.sh.
set -euo pipefail

DESKTOP_FILE="$HOME/.local/share/applications/log-inferer.desktop"

if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "Removed: $DESKTOP_FILE"
else
    echo "No launcher installed at $DESKTOP_FILE"
fi

command -v update-desktop-database >/dev/null 2>&1 && \
    update-desktop-database "$HOME/.local/share/applications" >/dev/null 2>&1 || true
