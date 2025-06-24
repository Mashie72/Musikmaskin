import tkinter as tk
import simpleaudio as sa
import threading
import os

STEMS = ["vocals", "drums", "bass", "other"]

class StemPlayer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.audio = sa.WaveObject.from_wave_file(filepath)
        self.play_obj = None
        self.is_muted = False
        self.is_solo = False
        self.is_playing = False

    def play(self):
        if not self.is_muted and not self.is_playing:
            self.play_obj = self.audio.play()
            self.is_playing = True

    def stop(self):
        if self.play_obj:
            self.play_obj.stop()
        self.is_playing = False

    def toggle_mute(self):
        self.is_muted = not self.is_muted

    def toggle_solo(self):
        self.is_solo = not self.is_solo

class MultiTrackApp:
    def __init__(self, root, folder):
        self.root = root
        self.folder = folder
        self.players = {}

        self.solo_mode = False

        for stem in STEMS:
            path = os.path.join(folder, f"{stem}.wav")
            if os.path.exists(path):
                self.players[stem] = StemPlayer(path)

        self.draw_ui()

    def draw_ui(self):
        self.root.title("4-kanals uppspelare (simpleaudio)")
        for i, (stem, player) in enumerate(self.players.items()):
            tk.Label(self.root, text=stem).grid(row=i, column=0)

            tk.Button(self.root, text="Play", command=lambda s=stem: self.play_stem(s)).grid(row=i, column=1)
            tk.Button(self.root, text="Stop", command=lambda s=stem: self.stop_stem(s)).grid(row=i, column=2)
            tk.Button(self.root, text="Mute", command=lambda s=stem: self.toggle_mute(s)).grid(row=i, column=3)
            tk.Button(self.root, text="Solo", command=lambda s=stem: self.toggle_solo(s)).grid(row=i, column=4)

        tk.Button(self.root, text="Stop All", command=self.stop_all).grid(row=len(self.players), column=1, columnspan=2)

    def play_stem(self, stem):
        player = self.players[stem]

        if self.solo_mode and not player.is_solo:
            return  # Ignorera om inte solo

        threading.Thread(target=player.play).start()

    def stop_stem(self, stem):
        self.players[stem].stop()

    def stop_all(self):
        for player in self.players.values():
            player.stop()

    def toggle_mute(self, stem):
        self.players[stem].toggle_mute()

    def toggle_solo(self, stem):
        self.players[stem].toggle_solo()
        self.solo_mode = any(p.is_solo for p in self.players.values())

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Användning: python3 multitrack_player_simpleaudio.py /sökväg/till/wav-map")
        sys.exit(1)

    folder = sys.argv[1]

    root = tk.Tk()
    app = MultiTrackApp(root, folder)
    root.mainloop()

