"""Smoke test for the one non-trivial bit of logic: stripping <think> blocks."""
from inferer import strip_thinking


def test_strip_thinking():
    raw = "<think>pondering the stack trace...</think>Root cause: disk full."
    assert strip_thinking(raw) == "Root cause: disk full."
    assert strip_thinking("no think tags here") == "no think tags here"
    multi = "<think>a</think>mid<think>b</think>end"
    assert strip_thinking(multi) == "midend"


if __name__ == "__main__":
    test_strip_thinking()
    print("ok")
