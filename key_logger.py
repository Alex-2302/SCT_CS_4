#!/usr/bin/env python3
"""
Foreground keyboard-event logger (educational).

- Captures keyboard events only while this window is focused.
- Shows keys live in the GUI.
- Appends each event to a CSV file with timestamp and a readable key label.
- Close the window to stop logging.

This is intended for ethical learning on your own machine only.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import csv
from datetime import datetime
import os

LOG_CSV = "keys_log.csv"

def readable_key(event):
    """Return a readable representation of the key for display/logging."""
    # event.char is the printable character (empty for e.g. Shift)
    if event.char and event.char != '\x00':
        return event.char
    # fallback to keysym (e.g. "Shift_L", "Return", "Escape", "Left")
    return f"[{event.keysym}]"

def log_key(key_label):
    """Append a row to the CSV log (timestamp, key)."""
    header_needed = not os.path.exists(LOG_CSV)
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["timestamp", "key"])
        writer.writerow([datetime.utcnow().isoformat() + "Z", key_label])

def on_key(event):
    key_label = readable_key(event)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # show in GUI
    txt.insert(tk.END, f"{timestamp}  {key_label}\n")
    txt.see(tk.END)
    # log to csv
    log_key(key_label)

def on_close():
    if messagebox.askokcancel("Quit", "Stop logging and close the app?"):
        root.destroy()

def clear_view():
    txt.delete("1.0", tk.END)

def open_log_location():
    # Inform user where the file is saved
    path = os.path.abspath(LOG_CSV)
    messagebox.showinfo("Log file", f"CSV log saved to:\n{path}")

# --- Build GUI ---
root = tk.Tk()
root.title("Foreground Key Logger — Educational")
root.geometry("700x450")
root.protocol("WM_DELETE_WINDOW", on_close)

label = tk.Label(root, text="This app captures keys ONLY while it is focused.\nPress keys here or anywhere while this window has focus.", justify="left")
label.pack(padx=10, pady=(10,0), anchor="w")

txt = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=18)
txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
txt.insert(tk.END, "Timestamp                Key\n")
txt.insert(tk.END, "------------------------------\n")

btn_frame = tk.Frame(root)
btn_frame.pack(fill=tk.X, padx=10, pady=(0,10))

clear_btn = tk.Button(btn_frame, text="Clear View", command=clear_view)
clear_btn.pack(side=tk.LEFT)

open_btn = tk.Button(btn_frame, text="Show Log Location", command=open_log_location)
open_btn.pack(side=tk.LEFT, padx=(8,0))

note_lbl = tk.Label(btn_frame, text="Close window to stop logging.", anchor="e")
note_lbl.pack(side=tk.RIGHT)

# Bind key events to the top-level window so it catches keys when focused
root.bind_all("<Key>", on_key)

# Run the app
root.mainloop()
