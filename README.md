# Clipboard Typer

A small desktop utility for typing clipboard contents into remote systems that
do not allow copy/paste. Built with Python and Tkinter.

## Use Case

Useful when working with web-based interfaces for remote systems (KVM consoles,
DRAC/iLO, VNC, etc.) where the clipboard is not shared with the host. The tool
reads your local clipboard and simulates keystrokes with a configurable delay to
avoid overrunning the input buffer.

## Features

- Simulates typing of clipboard contents with adjustable keystroke delay
- Configurable start delay to give you time to focus the target window
- Live highlighting in the clipboard preview shows typing progress
- Stop button to abort mid-typing
- 10 quick-access slots for frequently used strings (IPs, commands, passwords, etc.)
- Clicking a slot copies it to the clipboard; previous clipboard content is saved
  to the next empty slot automatically.
- Save and load slot profiles as JSON files (Don't save your passwords dude)
- Clipboard preview with character count

## Requirements

- Python 3.7+
- pyautogui
- pyperclip

Install dependencies:

```
pip install pyautogui pyperclip
```

### Linux

Tkinter may need to be installed separately:

```
sudo apt install python3-tk
```

### macOS

Tkinter is included with the Python installer from python.org. If you installed
Python via Homebrew:

```
brew install python-tk
```

pyautogui requires accessibility permissions to simulate keystrokes. Go to
System Settings > Privacy & Security > Accessibility and enable access for your
terminal or IDE.

### Windows

No additional setup required beyond the pip packages.

## Usage

```
python clipboard_typer.py
```

1. Copy text to your clipboard on the host machine.
2. Click into the target remote window.
3. Press "Type Clipboard" — the start delay gives you time to switch focus.
4. The tool will type the clipboard contents one character at a time.

Use the quick slots to store frequently used strings. Slot contents persist
between sessions when saved to a JSON profile file.

## Notes

Only printable ASCII characters (32-126) plus newlines and tabs are typed.
Non-ASCII characters are silently skipped to avoid pyautogui errors. The
clipboard preview will still show the original content so you can see if
anything will be dropped before committing to typing.