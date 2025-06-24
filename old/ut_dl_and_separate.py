import os
import subprocess
import sys

def download_audio(youtube_url, output_dir):
    print(f"\n🔻 Laddar ner: {youtube_url}")
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", f"{output_dir}/%(title)s.%(ext)s",
        youtube_url
    ]
    subprocess.run(command, check=True)
    print("✅ Ljudet är nedladdat.")

def separate_stems(input_path):
    print(f"\n🎚️ Kör Demucs på: {input_path}")
    command = [
        "demucs",
        "--two-stems", "vocals",  # ändra till "all" om du vill ha alla spår
        input_path
    ]
    subprocess.run(command, check=True)
    print("✅ Separation klar!")

def main():
    youtube_url = input("🎵 Klistra in YouTube-länk: ").strip()
    if not youtube_url:
        print("❌ Ingen länk angiven.")
        sys.exit(1)

    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    # Steg 1: Ladda ner
    download_audio(youtube_url, output_dir)

    # Hitta senaste nedladdade fil
    files = sorted(
        [f for f in os.listdir(output_dir) if f.endswith(".mp3")],
        key=lambda x: os.path.getmtime(os.path.join(output_dir, x)),
        reverse=True
    )
    if not files:
        print("❌ Ingen mp3-fil hittades.")
        sys.exit(1)

    latest_file = os.path.join(output_dir, files[0])
    print(f"\n🎧 Senaste ljudfilen: {latest_file}")

    # Steg 2: Separera stämmor
    separate_stems(latest_file)

if __name__ == "__main__":
    main()
