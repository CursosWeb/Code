### Descarga de audio de YouTube

Hay muchos módulos Python para descargar videos y audios de YouTube. Pero como la API de YouTube cambia muy frecuentemente, cada cierto tiempo hay que probar si las soluciones que se usaban siguen funcionando, y quizás buscar nuevos módulos que funcionen.

**Primera opción:**

Usando el módulo pytubefix. Para la mayoría de los videos hace falta autenticarse en YouTube, usando el navegador (ejecuta el script, y sigue instrucciones).

* Descarga el canal de audio de un video de YouTube: [ytaudio.py](ytaudio.py)
* Dependencias: [pytubefix](https://pytubefix.readthedocs.io/)

```commandline
pip install pytubefix
```

** Segunda opción:**

Usando el módulo yt-dlp. No hace falta autenticarse en YouTube (simplemente, ejecuta el script).

* Descarga el canal de audio de un video de YouTube: [ytaudio2.py](ytaudio2.py)
* Dependencias: [yt-dlp](https://github.com/yt-dlp/yt-dlp)

```commandline
pip install yt-dlp
```

