import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from time import ctime

r = sr.Recognizer()


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            alexis_speak(ask)
        # audio = r.listen(source)
        audio = r.listen(source, phrase_time_limit=5)

        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Waiting...")
            # alexis_speak("Sorry, I did not get that")
        except sr.RequestError:
            alexis_speak("Sorry, my speech service is down")
        return voice_data


def alexis_speak(audio_string):
    tts = gTTS(text=audio_string, lang="en")
    r = random.randint(1, 10000000)
    audio_file = "audio-" + str(r) + ".mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    if "what is your name" in voice_data:
        alexis_speak("My name is Alexis")
    if "what is the date" in voice_data:
        alexis_speak(ctime())
    if "search" in voice_data:
        search = record_audio("Search for?")
        url = f"https://google.com/search?q={search}"
        webbrowser.get().open(url)
        alexis_speak(f"Here is what I found for {search}")
    if "find location" in voice_data:
        location = record_audio("What is the location?")
        url = f"https://google.nl/maps/place/{location}"
        webbrowser.get().open(url)
        alexis_speak(f"Here is the location of {location}")
    if "exit" in voice_data:
        alexis_speak("Exiting program")
        exit()


time.sleep(1)
alexis_speak("How can I help you?")
while 1:
    voice_audio = record_audio()
    respond(voice_audio)
