#!/usr/bin/env python3

import yt_dlp

ytlink = "https://www.youtube.com/watch?v=84Tq-eAJIk4"

# Configuración para descargar solo el audio en la mejor calidad
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s', # Nombre del archivo = título del video
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    print("Iniciando descarga segura...")
    ydl.download([ytlink])
