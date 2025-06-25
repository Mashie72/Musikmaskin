# Musikmaskin

Detta lilla program tar en Youtube länk och extraherar Audio till MP.3
Sedan kör en valbar spårseparation med hjälp av python libbet DEMUCS som använder AI modeller för att sortera ut sång bas trummor och övrigt. 
Dessa hamnar under Separated mappen som Wav filer
I downloadsmappen sparas MP3 filen

Kända problem
- Du måste manuellt flytta MP3 filen från downloads till MP3 archive mappen (eller radera MP3 filen) innan du kan göra en ny stämseparation.
- Open output folder knappen fungerar ej.

Vad behöver du för att köra python programmet?
Python saker (använd installationsinstruktionerna längre ner för att få rätt versioner mm)
- tkinter , för GUI
- Numpy under version 2.0 , DEMUCS använder detta
- DEMUCS , AI stämseparatorn
- YT-dlp , För att konvertera YT streams till filer.

System
- ffmpeg , MPEG mm encoder måste installeras i systemet med "sudo apt install ffmpeg" eller liknande beroede på ditt system.

Installationsinstruktioner
- Använd någon Linux/Unix med support för X grafiskt gränssnitt (jag har testat på Mac, RaspberryPi  samt Windows WSL) 
(För att installera Windows WSL (öppna CMD som admin och kör: wsl --install)
- Windows WSL saknar X server per default, så tkinter (GUI motorn) kommer inte fungera om du inte också installerar en X server i Windows.
- Det bör i princip fungera på Windows "native" också, då skippar du WSL installationen ovan och du fårmladda ner python från python.org's webplats, då kommer (troligen) GUI't fungera utan extra förberedelser.
- Installera Git sudo apt update sudo apt install git
- klona repot:
bash
git clone https://github.com/Mashie72/Musikmaskin.git
cd Musikmaskin
- Skapa ett virtual environment för Python
(om du inte vill installera globalt)
bash
python3 -m venv .venv #notera att det är annan syntax för detta i CMD om du kör python i windows
source .venv/bin/activate #se ovan
- Installera alla paket från requirements.txt
bash
pip install -r requirements.txt
Det kommer installera exakt de paket (och versioner) som behövs
- Kör programmet 
bash
python3 yt_dl_sep_gui2.py
