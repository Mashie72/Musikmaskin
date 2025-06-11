# Musikmaskin

Detta lilla program tar en Youtube länk och extraherar Audio till MP.3
Sedan kör en valbar spårseparation med hjälp av python libbet DEMUCS som använder AI modeller för att sortera ut sång bas trummor och övrigt. 
Dessa hamnar under Separated mappen som Wav filer
I downloadsmappen sparas MP3 filen

- Kända problem
- Downloads mappen måste skapas manuellt första gången
- Du måste manuellt flytta MP3 filen från downloads till MP3 archive mappen (eller radera MP3 filen) innan du kan göra en ny stämseparation.
- Open output folder knappen fungerar ej.

Vad behöver du för att köra python programmet?
Python saker
- tkinter , för GUI
- Numpy under version 2.0 , DEMUCS använder detta
- DEMUCS , AI stämseparatorn
- YT-dlp , För att konvertera YT streams till filer.

System
- ffmpeg , MPEG mm encoder måste installeras i systemet med "sudo apt install ffmpeg" eller liknande beroede på ditt system.


