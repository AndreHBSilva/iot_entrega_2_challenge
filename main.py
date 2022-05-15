from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pygame
import speech_recognition as sr
import pyttsx3


def falar(texto, language='pt'):
  mp3_fo = BytesIO()
  tts = gTTS(texto, lang=language)
  tts.write_to_fp(mp3_fo)
  pygame.mixer.music.load(mp3_fo, 'mp3')
  pygame.mixer.music.play()
  
def detectarPeriodoDoDia():
  hora = datetime.today().strftime('%H')
  hora = int(hora)
  if hora <= 12:
    return 'Bom dia'
  elif hora <= 17:
    return 'Boa tarde'
  else:
    return 'Boa noite'

def cadastrarEventoAgenda():
  falar('Cadastrando evento na agenda...')
  return 'Cadastrando evento na agenda...'

def lerAgenda():
  falar('Lendo agenda...')
  return 'Lendo agenda...'

def checarHoras():
  falar('Checando horas...')
  return 'Checando horas...'

def mapearComandos(comando):
  comandos = {
    ('ler agenda', 'ver agenda', 'quero ver agenda', 'quero ler minha agenda', 'abrir agenda'): lerAgenda,
    ('cadastrar evento na agenda', 'cadastrar novo evento na agenda', 'cadastrar evento'): cadastrarEventoAgenda,
    ('checar as horas', 'que horas são', 'checar horário'): checarHoras
  }
  for key, value in comandos.items():
    if comando.lower() in key:
      return value()
    
def ouvir(recon):
  print('Fale algo...')
  audio = recon.listen(source)
  print('Reconhecendo...')
  comando = recon.recognize_google(audio, language='pt')
  return comando


recon = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()
with sr.Microphone() as source:
  recon.adjust_for_ambient_noise(source, duration=4)
  while True:
    try:
      comando = ouvir(recon)
      if 'sexta-feira' in comando:
        falar(detectarPeriodoDoDia()+', mestre. Como posso ajudá-lo?')
        print(comando)
        esperar = input('Pressione Enter para continuar...')
        comando = ouvir(recon)
        mapearComandos(comando)
        print(comando)
        esperar = input('Pressione Enter para continuar...')
    except sr.UnknownValueError:
      print('\nTente novamente')
      continue
    except KeyboardInterrupt:
      print('\nEncerrando...')
      break
    except KeyError:
      print('\n Comando não encontrado')
      continue

#print('hello world')