import pyttsx3
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import speech_recognition as sr
import pygame
import pyttsx3
import random
import json

# file = open('carteira.json', 'r')
# data = json.load(file)
# data["cartoes"].append({'numero': '4716 6151 2634 4615', 'dataValidade': '22/02/2023', 'codigoSeguranca': '117'})
# print(data)
# file.close()
# file = open('carteira.json', 'w')
# json.dump(data, file)
# file.close()

teste = 'histórico de compras' in ('abrir histórico de compras', 'ver histórico de compras', 'histórico de compras')

print(teste)
