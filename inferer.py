"""Backend: sends log text to a local Ollama model and returns a diagnosis."""
import json
import re
import urllib.error
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:8b"

SYSTEM_PROMPT = (
    "You are an expert systems engineer who diagnoses error logs from any "
    "source: Linux, Windows, macOS, servers, applications, drivers, games, etc. "
    "Given a log excerpt, identify:\n"
    "1. The most likely root cause\n"
    "2. The affected component or subsystem\n"
    "3. Concrete steps to fix or investigate further\n"
    "4. Your confidence (low/medium/high)\n"
    "Be concise and specific. If the log is truncated or ambiguous, say so."
)

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_thinking(text):
    """Remove deepseek-r1's <think>...</think> reasoning block."""
    return _THINK_RE.sub("", text).strip()


def analyze_stream(log_text, on_token, cancel_event=None):
    """Stream a diagnosis for log_text from Ollama, calling on_token(str) per chunk.

    If cancel_event is set mid-stream, the request is dropped and the call returns early.
    """
    prompt = f"{SYSTEM_PROMPT}\n\n--- LOG ---\n{log_text}\n--- END LOG ---\n"
    payload = json.dumps({"model": MODEL, "prompt": prompt, "stream": True}).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            for line in resp:
                if cancel_event is not None and cancel_event.is_set():
                    return
                line = line.strip()
                if not line:
                    continue
                chunk = json.loads(line)
                if "error" in chunk:
                    raise RuntimeError(chunk["error"])
                on_token(chunk.get("response", ""))
                if chunk.get("done"):
                    break
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_URL} -- is `ollama serve` running? ({e})"
        ) from e
