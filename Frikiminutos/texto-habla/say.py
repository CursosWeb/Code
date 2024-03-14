#!/usr/bin/env python3

import pyttsx3
engine = pyttsx3.init()

engine.say("Hello!")
engine.runAndWait()

engine.say("Hello! This is a bit longer text")
engine.runAndWait()

# Set non-default rate
rate = 125
engine.setProperty('rate', rate)
engine.say(f"Hello! This is a bit longer text with a specific rate of {rate}")
engine.runAndWait()

# Set to a different voice (1 is female)
voices = engine.getProperty('voices')       #getting details of current voice
spanish_found = False
print("Voices: ", end='')
for voice in voices:
    print(voice.id, end=', ')
    if voice.id == 'spanish':
        spanish_found = True
if spanish_found:
    engine.setProperty('voice', voice)
    engine.say("¡Hola! Este es un texto con la voz española.")
else:
    engine.say("I coudln't find a spanish voice")
engine.runAndWait()

# Write to a file (needs espeak and ffmpeg)
engine.save_to_file('Hello World', 'hello.mp3')
engine.runAndWait()
