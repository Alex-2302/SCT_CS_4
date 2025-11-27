Safe Terminal Key Capture (Consent-Based)

A safe, ethical, and non-malicious terminal-based key capture tool built using Python’s curses module.
It records only the keys pressed inside the program window, and only after explicit user consent.
All keystrokes are displayed in a live terminal UI and saved to a timestamped log file.

This tool is great for:

UX / UI testing

Typing analysis

Educational demonstrations

Accessibility input research

Understanding how terminal key events work

Debugging keystroke handling in terminal apps

This project is NOT a system keylogger.
It does NOT capture system input, background input, or any input outside the program window.

Features

Live terminal interface

Displays each key vertically (one per line).

Shows current typed text in a horizontal bar at the bottom.

Infinite scrolling (no overflow errors).

Human-readable key names

Letter keys → a, b, h, o, w, etc.

Special keys → SPACE, ENTER, BACKSPACE, ESC

Clean log storage

All logs are stored in:

logs/


Each session generates a file like:

session_20251127_124130.txt

Fully consent-based

Program only starts after the user types:

yes

Safe by design

No background hooks

No system-wide logging

No stealth mode

No persistence

Only active inside the program window
Run the program:
python3 key_logger.py

Give consent:

When prompted:

Type YES to continue:


Type:

yes

Usage

Every key you press inside the terminal appears vertically on screen.

Your typed text appears as a single line at the bottom.

Press ESC to end the session.

Session logs will be inside:

logs/

Log File Example:

--- Session started 2025-11-27 12:41:30 ---
12:41:33 - h
12:41:33 - i
12:41:33 - SPACE
12:41:33 - h
12:41:34 - o
12:41:34 - w
...
12:41:57 - ESC
--- Session ended 2025-11-27 12:41:57 ---

Why Is This Important?

Key input handling is an essential part of:

Terminal UI design

Text editors

Command-line tools

Games

Accessibility systems

Developer tools

Research on human-computer interaction

This project helps students, researchers, and developers:

Understand low-level terminal input

Study how users type

Debug keystroke flow in apps

Build more responsive TUI applications

Demonstrate keystroke visualization safely

Unlike malicious keyloggers, this tool is transparent, consent-based, and locked to the program window, making it suitable for academic use and open-source distribution.
