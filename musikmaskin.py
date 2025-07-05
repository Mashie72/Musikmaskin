import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from yt_dlp import YoutubeDL
import shutil

# Hemkatalog
HOME_DIR = os.path.expanduser("~")
DOWNLOAD_DIR = os.path.join(HOME_DIR, "Musikmaskin", "downloads")
ARCHIVE_DIR = os.path.join(DOWNLOAD_DIR, "mp3archive")



def download_audio(youtube_url):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'keepvideo': False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])


def find_latest_mp3():
    files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp3")]
    if not files:
        return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)), reverse=True)
    return os.path.join(DOWNLOAD_DIR, files[0])


def separate_stems(mp3_path, mode):
    if mode == "two":
        command = ["demucs", "--two-stems", "vocals", mp3_path]
    else:
        command = ["demucs", mp3_path]
    os.system(' '.join(f'"{arg}"' if ' ' in arg else arg for arg in command))


def is_wsl():
    return "microsoft" in os.uname().release.lower()

def open_output_folder():
    sep_dir = os.path.join(HOME_DIR, "Musikmaskin", "separated", "htdemucs")
    if not os.path.exists(sep_dir):
        messagebox.showerror("Fel", "Katalogen hittades inte:\n" + sep_dir)
        return

    if sys.platform.startswith("win"):
        os.startfile(sep_dir)
    elif sys.platform == "darwin":
        os.system(f"open '{sep_dir}'")
    elif is_wsl():
        os.system(f"explorer.exe '{sep_dir}'")
    else:
        os.system(f"xdg-open '{sep_dir}'")


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

        # Flytta MP3 till arkiv
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        shutil.move(mp3_path, os.path.join(ARCHIVE_DIR, os.path.basename(mp3_path)))

        status_label.config(text="✅ Klar! Klicka för att visa filer.")
        open_button.config(state="normal")

    except Exception as e:
        messagebox.showerror("Fel", f"Något gick fel:\n{e}")
        status_label.config(text="❌ Fel uppstod.")



# 🖼️ GUI
window = tk.Tk()
window.title("🎵 Musikmaskin")
window.geometry("500x280")
window.resizable(False, False)

# Font saker
default_font = ("Segoe UI", 11)
bold_font = ("Segoe UI", 12, "bold")

ttk.Label(window, text="YouTube-länk:").pack(pady=(10, 0))
url_entry = ttk.Entry(window, width=60)
url_entry.pack(pady=5)

# Radioknappar för stämval
stem_mode = tk.StringVar(value="two")
frame = ttk.Frame(window)
frame.pack()
ttk.Label(frame, text="🎚️ Separationsläge:", font=bold_font).pack(anchor="w")
ttk.Radiobutton(frame, text="🎙️ 2 stämmor (Sång + musik)", variable=stem_mode, value="two").pack(anchor="w")
ttk.Radiobutton(frame, text="🎛️ 4 stämmor (Sång, trummor, bas, övrigt)", variable=stem_mode, value="four").pack(anchor="w")

ttk.Button(window, text="Ladda ner och separera", command=run_process).pack(pady=5)

open_button = tk.Button(window, text="📂 Öppna utdatan", command=open_output_folder, state="disabled")
open_button.pack(pady=5)

status_label = ttk.Label(window, text="")
status_label.pack()

window.mainloop()

