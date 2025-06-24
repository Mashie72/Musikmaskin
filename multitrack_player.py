import sys
import os
import tkinter as tk
import threading
import pygame

STEMS = ["vocals", "drums", "bass", "other"]

def play_stem(path):
    def _play():
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    threading.Thread(target=_play).start()

def create_gui(folder):
    pygame.mixer.init()
    root = tk.Tk()
    root.title("4-kanals spelare")

    for stem in STEMS:
        path = os.path.join(folder, f"{stem}.wav")
        if os.path.exists(path):
            btn = tk.Button(root, text=f"Spela {stem}", command=lambda p=path: play_stem(p))
            btn.pack(padx=10, pady=5)
        else:
            tk.Label(root, text=f"{stem}.wav hittades ej.").pack()

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Användning: python3 multitrack_player.py /sökväg/till/stämmor")
        sys.exit(1)
    create_gui(sys.argv[1])

