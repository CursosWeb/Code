#!/usr/bin/env python3

import pytube

ytlink = "https://www.youtube.com/watch?v=r3dNIF6lq54"

video = pytube.YouTube(ytlink)
audio = video.streams.filter(only_audio=True, file_extension='webm').first()
audio.download()
