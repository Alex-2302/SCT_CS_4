#!/usr/bin/env python3
"""
Safe, consent-based terminal key capture (curses).
- Logs to ./logs/session_YYYYmmdd_HHMMSS.txt
- Shows fixed heading "Your input here:" at top (no input bar)
- Displays each key pressed vertically (one per line)
- Scrolls when needed (infinite entry)
- Press ESC to stop
"""

import curses
import time
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Map some special key codes to names
SPECIAL_KEYS = {
    27: "ESC",
    10: "ENTER",
    13: "ENTER",
    32: "SPACE",
    curses.KEY_BACKSPACE if hasattr(curses, "KEY_BACKSPACE") else -1: "BACKSPACE",
    127: "BACKSPACE",
    curses.KEY_LEFT if hasattr(curses, "KEY_LEFT") else -1: "LEFT",
    curses.KEY_RIGHT if hasattr(curses, "KEY_RIGHT") else -1: "RIGHT",
    curses.KEY_UP if hasattr(curses, "KEY_UP") else -1: "UP",
    curses.KEY_DOWN if hasattr(curses, "KEY_DOWN") else -1: "DOWN",
    curses.KEY_DC if hasattr(curses, "KEY_DC") else -1: "DELETE",
    curses.KEY_HOME if hasattr(curses, "KEY_HOME") else -1: "HOME",
    curses.KEY_END if hasattr(curses, "KEY_END") else -1: "END",
    curses.KEY_PPAGE if hasattr(curses, "KEY_PPAGE") else -1: "PGUP",
    curses.KEY_NPAGE if hasattr(curses, "KEY_NPAGE") else -1: "PGDN",
}

def readable_key_name(key):
    """Return a human readable name for the given integer key code."""
    # direct lookup for known special values
    if key in SPECIAL_KEYS and SPECIAL_KEYS[key] != -1:
        return SPECIAL_KEYS[key]
    # curses may return values >= 256 for special names, try to use curses.keyname
    try:
        name = curses.keyname(key).decode('utf-8')
        # curses.keyname returns things like '^M', 'KEY_LEFT', or literal characters
        # Normalize common outputs
        if name.startswith("KEY_"):
            return name  # e.g. KEY_LEFT
        if len(name) == 1:
            return name  # printable single char
        # keep it as-is otherwise
        return name
    except Exception:
        pass
    # fallback: printable char
    try:
        ch = chr(key)
        if ch.isprintable():
            return ch
    except Exception:
        pass
    # last resort
    return f"KEY_{key}"

def main(stdscr):
    # Basic curses setup
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(False)  # blocking getch()
    stdscr.keypad(True)    # enable special keys
    stdscr.scrollok(True)  # allow scrolling when adding lines at bottom

    # Prepare log file
    session_start = datetime.now()
    log_path = os.path.join(LOG_DIR, f"session_{session_start.strftime('%Y%m%d_%H%M%S')}.txt")
    logf = open(log_path, "w", encoding="utf-8")
    logf.write(f"--- Session started {session_start} ---\n")

    # Header lines (fixed)
    title = "SAFE KEY CAPTURE (Terminal Only)"
    consent_hint = "Press keys... ESC to stop."
    input_heading = "Your input here:"  # user requested single fixed comment at top

    # Initial layout
    stdscr.erase()
    height, width = stdscr.getmaxyx()

    try:
        stdscr.addnstr(0, 0, title, width - 1)
        stdscr.addnstr(1, 0, consent_hint, width - 1)
        stdscr.addnstr(2, 0, input_heading, width - 1)
    except curses.error:
        # ignore add errors for tiny windows; we'll still try to run
        pass

    # Start printing keys at row 4 (vertical list)
    vertical_y = 4

    # Keep reconstructed user input (for the final "user input:" line in the log)
    reconstructed = []

    while True:
        # update dimensions (in case terminal was resized)
        height, width = stdscr.getmaxyx()

        # read a key (blocking)
        key = stdscr.getch()
        timestamp = time.strftime("%H:%M:%S")

        key_name = readable_key_name(key)

        # Update reconstructed text for printable chars and BACKSPACE handling
        if key_name in ("BACKSPACE",):
            # remove last character if any
            if reconstructed:
                reconstructed.pop()
        elif key_name == "ENTER":
            # represent ENTER in reconstructed as newline (we store '\n')
            reconstructed.append("\n")
        elif key_name == "SPACE":
            reconstructed.append(" ")
        elif key_name == "ESC":
            # log then break
            logf.write(f"{timestamp} - {key_name}\n")
            logf.flush()
            break
        else:
            # if key_name is a single printable char, append it
            if len(key_name) == 1 and key_name.isprintable():
                reconstructed.append(key_name)
            else:
                # non-printable / named key: do not add to reconstructed text
                pass

        # Write log line
        logf.write(f"{timestamp} - {key_name}\n")
        logf.flush()

        # Display vertically at left side
        display_text = key_name

        # Make sure we don't attempt to write past the bottom: if vertical_y is beyond (height-1),
        # scroll up by one and set vertical_y to height-2 so new line appears at bottom-1
        if vertical_y >= height - 1:
            try:
                stdscr.scroll(1)
            except curses.error:
                # if scroll fails, just reset screen (best-effort)
                stdscr.erase()
                try:
                    stdscr.addnstr(0, 0, title, width - 1)
                    stdscr.addnstr(1, 0, consent_hint, width - 1)
                    stdscr.addnstr(2, 0, input_heading, width - 1)
                except curses.error:
                    pass
            vertical_y = height - 2  # bottom-most writable row minus input heading area

        # Safe add: truncate to width-1 to avoid addstr errors
        try:
            stdscr.addnstr(vertical_y, 0, display_text, width - 1)
        except curses.error:
            # ignore single write errors (very small terminal), continue
            pass
        vertical_y += 1

        # Refresh screen
        try:
            stdscr.refresh()
        except curses.error:
            pass

    # End session: write reconstructed user input to log as a single string
    session_end = datetime.now()
    logf.write(f"--- Session ended {session_end} ---\n")
    # produce a single-line representation for the reconstructed input:
    # replace newlines with literal '\n', keep spaces visible
    user_input_repr = "".join(reconstructed).replace("\n", "\\n")
    logf.write(f"user input: {user_input_repr}\n")
    logf.close()

if __name__ == "__main__":
    print("This program captures keys ONLY inside this terminal window.")
    consent = input("Type YES to continue: ").strip().lower()
    if consent != "yes":
        print("Exiting (no consent).")
        exit(0)

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        # allow Ctrl-C to exit gracefully
        print("\nInterrupted.")
    print("Session ended. Logs saved to ./logs/")

