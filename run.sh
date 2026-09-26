#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 -c "import tkinter" 2>/dev/null || {
    echo "tkinter not found. Install it first, e.g.:"
    echo "  sudo apt install python3-tk     # Debian/Ubuntu"
    echo "  sudo pacman -S tk                # Arch"
    echo "  sudo dnf install python3-tkinter # Fedora"
    exit 1
}

exec python3 main.py
