#!/usr/bin/env bash
set -euo pipefail

if ! command -v ollama >/dev/null 2>&1; then
    echo "ollama not found. Install it first:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

if ! pgrep -x ollama >/dev/null 2>&1; then
    echo "Starting ollama serve in the background..."
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 2
fi

echo "Pulling deepseek-r1:8b (this may take a while)..."
ollama pull deepseek-r1:8b
