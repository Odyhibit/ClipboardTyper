import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import json
from tkinter import filedialog
import pyperclip
import pyautogui
import threading
import time

SLOT_COUNT = 6


def save_slots():
    path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if path:
        with open(path, 'w') as f:
            json.dump([var.get() for var in slot_vars], f, indent=2)

def load_slots():
    path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if path:
        with open(path, 'r') as f:
            data = json.load(f)
        for i, var in enumerate(slot_vars):
            var.set(data[i] if i < len(data) else "")

def get_clipboard():
    try:
        return pyperclip.paste()
    except:
        return ""

def set_clipboard(text):
    try:
        pyperclip.copy(text)
    except:
        pass

def find_empty_slot():
    for i, var in enumerate(slot_vars):
        if var.get().strip() == "":
            return i
    return None

def slot_clicked(i):
    text = slot_vars[i].get()
    if not text.strip():
        return
    current = get_clipboard()
    if current.strip():
        already_saved = any(var.get() == current for var in slot_vars)
        if not already_saved:
            empty = find_empty_slot()
            if empty is not None:
                slot_vars[empty].set(current)
    set_clipboard(text)

def clear_slot(i):
    slot_vars[i].set("")

def refresh_display():
    content = get_clipboard()
    char_count.set(f"{len(content)} characters")
    text_box.config(state='normal')
    text_box.delete('1.0', tk.END)
    text_box.insert('1.0', content)
    text_box.tag_remove('highlight', '1.0', tk.END)
    text_box.config(state='disabled')

def auto_refresh():
    if not is_typing:
        refresh_display()
    root.after(1000, auto_refresh)

def set_highlight(index):
    text_box.config(state='normal')
    text_box.tag_remove('highlight', '1.0', tk.END)
    if index >= 0:
        pos = f"1.0 + {index} chars"
        text_box.tag_add('highlight', pos, f"{pos} + 1 chars")
        text_box.see(pos)
    text_box.config(state='disabled')


def delayed_paste():
    global is_typing, stop_requested
    stop_requested = False
    delay_secs = delay_var.get() / 10000.0
    start_delay = start_delay_var.get()

    for i in range(start_delay, 0, -1):
        if stop_requested:
            root.after(0, reset_button)
            return
        root.after(0, lambda n=i: type_btn.config(
            text=f"Starting in {n}s...", bg='#e8a020'))
        time.sleep(1)

    text = get_clipboard()
    if not text:
        root.after(0, reset_button)
        return

    safe_text = ''.join(c for c in text if 32 <= ord(c) <= 126 or c in '\n\t')

    is_typing = True
    root.after(0, lambda: stop_btn.pack(side='right', padx=5))
    root.after(0, lambda: type_btn.config(text="● Typing...", bg='#c0392b'))

    for idx, char in enumerate(safe_text):
        if stop_requested:
            break
        root.after(0, lambda i=idx: set_highlight(i))
        pyautogui.typewrite(char, interval=0)
        time.sleep(delay_secs)

    root.after(0, lambda: set_highlight(-1))
    is_typing = False
    root.after(0, lambda: stop_btn.pack_forget())
    root.after(0, reset_button)

def request_stop():
    global stop_requested
    stop_requested = True

def reset_button():
    type_btn.config(text="▶  Type Clipboard", bg='#4a7', fg='white')

def start_typing():
    threading.Thread(target=delayed_paste, daemon=True).start()

# --- Build UI ---
root = tk.Tk()
root.title("Clipboard Typer")
is_typing = False
stop_requested = False

# --- Quick Slots ---
slots_frame = tk.LabelFrame(root, text="Quick Slots", padx=5, pady=5)
slots_frame.pack(fill='x', padx=10, pady=(10, 0))

slot_vars = []
for i in range(SLOT_COUNT):
    row = tk.Frame(slots_frame)
    row.pack(fill='x', pady=1)

    var = tk.StringVar()
    slot_vars.append(var)

    lbl = tk.Label(row, text=f"{i+1:2}.", width=3, anchor='e')
    lbl.pack(side='left')

    entry = tk.Entry(row, textvariable=var)
    entry.pack(side='left', padx=(2, 4), fill='x', expand=True)
    entry.bind("<Button-1>", lambda e, idx=i: slot_clicked(idx))

    clear_btn = tk.Button(row, text="✕", width=2, fg='red',
                          command=lambda idx=i: clear_slot(idx))
    clear_btn.pack(side='left')

# --- Clipboard Viewer ---
viewer_frame = tk.LabelFrame(root, text="Clipboard Preview", padx=5, pady=5)
viewer_frame.pack(fill='both', expand=True, padx=10, pady=(10, 0))

text_box = ScrolledText(viewer_frame, width=60, height=10, state='disabled')
text_box.pack(fill='both', expand=True)
text_box.tag_config('highlight', background='#f0e040', foreground='black')

char_count = tk.StringVar(value="0 characters")
tk.Label(viewer_frame, textvariable=char_count, anchor='e').pack(fill='x')

# --- Row 1: Sliders ---
slider_frame = tk.Frame(root)
slider_frame.pack(fill='x', padx=10, pady=(8, 2))

tk.Label(slider_frame, text="Delay(s):").pack(side='left')
start_delay_var = tk.IntVar(value=3)
tk.Scale(slider_frame, from_=1, to=100, orient='horizontal',
         variable=start_delay_var, length=100).pack(side='left', padx=(0, 15))

tk.Label(slider_frame, text="Keystroke(ms):").pack(side='left')
delay_var = tk.IntVar(value=50)
tk.Scale(slider_frame, from_=1, to=200, orient='horizontal',
         variable=delay_var, length=150).pack(side='left', padx=(0, 15))

# --- Row 2: Buttons ---
btn_frame = tk.Frame(root)
btn_frame.pack(fill='x', padx=10, pady=(10, 8))

tk.Button(btn_frame, text="💾 Save", command=save_slots).pack(side='left', padx=5)
tk.Button(btn_frame, text="📂 Load", command=load_slots).pack(side='left', padx=5)

stop_btn = tk.Button(btn_frame, text="■  Stop",
                     command=request_stop,
                     bg='#c0392b', fg='white', padx=8)
# hidden until typing starts

type_btn = tk.Button(btn_frame, text="▶  Type Clipboard",
                     command=start_typing,
                     bg='#4a7', fg='white', padx=8)
type_btn.pack(side='right', padx=5)

auto_refresh()
root.mainloop()