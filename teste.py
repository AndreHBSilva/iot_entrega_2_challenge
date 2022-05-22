import pyttsx3
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import speech_recognition as sr
import pygame
import pyttsx3
import random
import json

engine = pyttsx3.init()
recon = sr.Recognizer()
recon.energy_threshold = 50
recon.dynamic_energy_threshold = False
pygame.mixer.init()

def falar(texto, language='pt'):
  mp3_fo = BytesIO()
  tts = gTTS(texto, lang=language)
  tts.write_to_fp(mp3_fo)
  pygame.mixer.music.load(mp3_fo, 'mp3')
  pygame.mixer.music.play()
  #engine.runAndWait()

file = open("agenda.txt", "r").read().replace("\n", " ")
falar(str(file))
entrada = input()
