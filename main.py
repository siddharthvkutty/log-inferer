#!/usr/bin/env python3
"""Log Inferer -- paste or load an error log, get an AI diagnosis via local Ollama."""
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from inferer import MODEL, analyze_stream

BG = "#1e1e2e"
PANEL = "#181825"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
ACCENT_DIM = "#45475a"
FONT = ("DejaVu Sans Mono", 11)
FONT_UI = ("DejaVu Sans", 10)


class LogInfererApp:
    def __init__(self, root):
        self.root = root
        root.title("Log Inferer")
        root.geometry("1000x700")
        root.configure(bg=BG)

        self.queue = queue.Queue()

        self._build_ui()
        self.root.after(80, self._poll_queue)

    def _build_ui(self):
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=12, pady=(12, 6))

        tk.Label(top, text="Log Inferer", bg=BG, fg=ACCENT,
                 font=("DejaVu Sans", 16, "bold")).pack(side="left")
        tk.Label(top, text=f"  ·  model: {MODEL}", bg=BG, fg=ACCENT_DIM,
                 font=FONT_UI).pack(side="left")

        btns = tk.Frame(top, bg=BG)
        btns.pack(side="right")
        self._button(btns, "Open File...", self.browse_file).pack(side="left", padx=4)
        self.analyze_btn = self._button(btns, "Analyze", self.analyze, accent=True)
        self.analyze_btn.pack(side="left", padx=4)
        self._button(btns, "Clear", self.clear).pack(side="left", padx=4)

        body = tk.PanedWindow(self.root, bg=BG, orient="vertical", sashwidth=6,
                               bd=0, sashrelief="flat")
        body.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        in_frame = tk.Frame(body, bg=BG)
        tk.Label(in_frame, text="LOG INPUT (paste text or open a file)", bg=BG,
                 fg=ACCENT_DIM, font=FONT_UI, anchor="w").pack(fill="x")
        self.input_text = tk.Text(in_frame, bg=PANEL, fg=FG, insertbackground=FG,
                                   font=FONT, wrap="none", undo=True,
                                   relief="flat", padx=10, pady=10)
        self.input_text.pack(fill="both", expand=True, pady=(4, 0))
        body.add(in_frame, height=300)

        out_frame = tk.Frame(body, bg=BG)
        tk.Label(out_frame, text="DIAGNOSIS", bg=BG, fg=ACCENT_DIM,
                 font=FONT_UI, anchor="w").pack(fill="x")
        self.output_text = tk.Text(out_frame, bg=PANEL, fg=FG, font=FONT,
                                    wrap="word", state="disabled", relief="flat",
                                    padx=10, pady=10)
        self.output_text.pack(fill="both", expand=True, pady=(4, 0))
        body.add(out_frame, height=300)

        self.status = tk.Label(self.root, text="Ready", bg=BG, fg=ACCENT_DIM,
                                font=FONT_UI, anchor="w")
        self.status.pack(fill="x", padx=14, pady=(0, 8))

    def _button(self, parent, text, cmd, accent=False):
        return tk.Button(parent, text=text, command=cmd,
                          bg=ACCENT if accent else ACCENT_DIM,
                          fg="#11111b" if accent else FG,
                          activebackground=ACCENT, activeforeground="#11111b",
                          font=FONT_UI, relief="flat", padx=12, pady=6,
                          cursor="hand2", bd=0)

    def browse_file(self):
        path = filedialog.askopenfilename(title="Open log file")
        if not path:
            return
        try:
            text = Path(path).read_text(errors="replace")
        except OSError as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")
            return
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", text)
        self.status.config(text=f"Loaded {path}")

    def clear(self):
        self.input_text.delete("1.0", "end")
        self._set_output("")
        self.status.config(text="Ready")

    def _set_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.config(state="disabled")

    def analyze(self):
        log_text = self.input_text.get("1.0", "end").strip()
        if not log_text:
            messagebox.showwarning("Empty log", "Paste a log or open a file first.")
            return
        self.analyze_btn.config(state="disabled", text="Thinking...")
        self.status.config(text=f"Querying {MODEL} via Ollama...")
        self._set_output("")

        threading.Thread(target=self._run_analysis, args=(log_text,), daemon=True).start()

    def _run_analysis(self, log_text):
        try:
            def on_token(tok):
                self.queue.put(("token", tok))
            analyze_stream(log_text, on_token)
            self.queue.put(("done", None))
        except Exception as e:
            self.queue.put(("error", str(e)))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.queue.get_nowait()
                if kind == "token":
                    self.output_text.config(state="normal")
                    self.output_text.insert("end", payload)
                    self.output_text.see("end")
                    self.output_text.config(state="disabled")
                elif kind == "done":
                    self.analyze_btn.config(state="normal", text="Analyze")
                    self.status.config(text="Done")
                elif kind == "error":
                    self.analyze_btn.config(state="normal", text="Analyze")
                    self.status.config(text=f"Error: {payload}")
                    messagebox.showerror("Inference failed", payload)
        except queue.Empty:
            pass
        self.root.after(80, self._poll_queue)


def main():
    root = tk.Tk()
    LogInfererApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
