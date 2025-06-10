import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

# Hemkatalog
HOME_DIR = os.path.expanduser("~/")
DOWNLOAD_DIR = os.path.join(HOME_DIR, "musikmaskin")

def download_audio(youtube_url):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    command = [
        "yt-dlp",
        "-k",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        youtube_url
    ]
    subprocess.run(command, check=True)
#Hej
#detta blir bra
#Branch testning

def find_latest_mp3():
    files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp3")]
    if not files:
        return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)), reverse=True)
    return os.path.join(DOWNLOAD_DIR, files[0])

def separate_stems(mp3_path, mode):
    if mode == "two":
        command = [
            "demucs",
            "--two-stems", "vocals",
            mp3_path
        ]
    else:  # mode == "four"
        command = [
            "demucs",
            mp3_path
        ]
    subprocess.run(command, check=True)

def open_output_folder():
    sep_dir = os.path.join(HOME_DIR, "separated")
    if os.path.exists(sep_dir):
        subprocess.run(["open", sep_dir])
    else:
        messagebox.showerror("Fel", "Ingen utdatamapp hittades.")

def run_process():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Obs", "Skriv in en YouTube-länk.")
        return

    try:
        status_label.config(text="⏳ Laddar ner...")
        window.update()
        download_audio(url)

        mp3_path = find_latest_mp3()
        if not mp3_path:
            messagebox.showerror("Fel", "Ingen MP3-fil hittades.")
            return

        status_label.config(text="🎚️ Separerar stämmor...")
        window.update()
        separate_stems(mp3_path, stem_mode.get())

        status_label.config(text="✅ Klar! Klicka för att visa filer.")
        open_button.config(state="normal")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fel", f"Något gick fel:\n{e}")
        status_label.config(text="❌ Fel uppstod.")

# 🖼️ GUI
window = tk.Tk()
window.title("🎵 Musikmaskin")
window.geometry("500x240")
window.resizable(False, False)

tk.Label(window, text="YouTube-länk:").pack(pady=(10, 0))
url_entry = tk.Entry(window, width=60)
url_entry.pack(pady=5)

# Radioknappar för stämval
stem_mode = tk.StringVar(value="two")
frame = tk.Frame(window)
frame.pack()
tk.Label(frame, text="🎛️ Separationsläge:").pack(anchor="w")
tk.Radiobutton(frame, text="🎙️ 2 stämmor (Sång + musik)", variable=stem_mode, value="two").pack(anchor="w")
tk.Radiobutton(frame, text="🎚️ 4 stämmor (Sång, trummor, bas, övrigt)", variable=stem_mode, value="four").pack(anchor="w")

tk.Button(window, text="Ladda ner och separera", command=run_process).pack(pady=5)

open_button = tk.Button(window, text="📂 Öppna utdatan", command=open_output_folder, state="disabled")
open_button.pack(pady=5)

status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()
