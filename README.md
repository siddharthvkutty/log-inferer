# Log Inferer

A small desktop tool that reads your error logs and tells you what's actually wrong with them.

Paste a log, or point it at a file — Linux kernel panics, Windows Event Viewer dumps, game crash logs, server tracebacks, whatever — and it streams back a diagnosis: likely root cause, affected component, what to do about it, and how confident it is. Runs entirely on your machine via [Ollama](https://ollama.com), no API keys, no data leaving your box.

## Requirements

- Python 3 with `tkinter` (usually a separate OS package)
  - Debian/Ubuntu: `sudo apt install python3-tk`
  - Arch: `sudo pacman -S tk`
  - Fedora: `sudo dnf install python3-tkinter`
- [Ollama](https://ollama.com) installed and running
- No Python packages to install — the GUI is stdlib `tkinter`, the backend is stdlib `urllib`

## Quick start

```bash
git clone <this-repo>
cd log-inferer

# one-time: pulls deepseek-r1:8b (starts ollama if it isn't running)
bash scripts/pull_model.sh

# launch the app
./run.sh
```

Paste a log into the top pane, or hit **Open File...** to load one from disk, then **Analyze**. The diagnosis streams in below as the model reasons through it.

## Project structure

```
log-inferer/
├── main.py               tkinter GUI
├── inferer.py             talks to the local Ollama API, builds the prompt
├── test_inferer.py        smoke test
├── run.sh                 launches the app
└── scripts/
    └── pull_model.sh       installs/starts ollama, pulls the model
```

## How it works

`inferer.py` sends your log text to `http://localhost:11434/api/generate` with a system prompt asking for root cause, affected component, fix steps, and confidence. Ollama streams tokens back; the GUI renders them live so you can watch the model reason through the log instead of staring at a frozen window.

## Model

Defaults to `deepseek-r1:8b` — a reasoning model, so it works through the log before answering rather than pattern-matching a guess. To use a different model, change `MODEL` in `inferer.py` and pull it with `ollama pull <name>` instead.

## License

No license file yet — add one (MIT is the usual default) before you rely on others being able to reuse this.
