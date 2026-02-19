#!/usr/bin/env python3

from pytubefix import YouTube

ytlink = "https://www.youtube.com/watch?v=84Tq-eAJIk4"

object = YouTube(ytlink, use_oauth=True, allow_oauth_cache=True)
print(object.title)
stream = object.streams.get_audio_only()
stream.download()
