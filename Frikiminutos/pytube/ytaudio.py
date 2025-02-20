#!/usr/bin/env python3

from pytubefix import YouTube

ytlink = "https://www.youtube.com/watch?v=r3dNIF6lq54"

object = YouTube(ytlink)
stream = object.streams.get_audio_only()
stream.download()
