import speech_recognition as sr
from os import path
from pydub import AudioSegment

                                                     
audio = AudioSegment.from_mp3("11.mp3")
audio.export("wav_format.wav", format="wav")

                                     
rec = sr.Recognizer()
with sr.AudioFile("wav_format.wav") as source:
        audio = rec.record(source)  # read the entire audio file                  

        print("Transcription: " + rec.recognize_google(audio))
