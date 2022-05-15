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

def cadastrarEventoAgenda(recon):
  try:
    falar('Ok, qual o nome do evento que devo cadastrar?')
    nomeEvento = ouvir(recon)
    engine.runAndWait()
    falar('Para qual dia?')
    diaEvento = ouvir(recon)
    engine.runAndWait()
    falar('Para que horas?')
    horarioEvento = ouvir(recon)
    engine.runAndWait()
    falar('Tudo certo, o seu evento foi cadastrado!')
    engine.runAndWait()
    f = open('agenda.txt', 'a', encoding='utf-8')
    f.write('Você tem o evento '+nomeEvento+' às '+horarioEvento+' no dia '+diaEvento+'\n')
    f.close()
  except OSError:
    print('Arquivo de agenda não encontrado')


def lerAgenda(recon):
  try:
    f = open('agenda.txt', 'r', encoding='utf-8')
    for line in f:
      falar(line)
    f.close()
  except OSError:
    print('Arquivo de agenda não encontrado')


def checarHoras(recon):
  falar('Checando horas...')
  return 'Checando horas...'

def mapearComandos(comando, recon):
  comandos = {
    ('ler agenda', 'ver agenda', 'quero ver agenda', 'quero ler minha agenda', 'abrir agenda'): lerAgenda,
    ('cadastrar evento na agenda', 'cadastrar novo evento na agenda', 'cadastrar evento'): cadastrarEventoAgenda,
    ('checar as horas', 'que horas são', 'checar horário'): checarHoras
  }
  for key, value in comandos.items():
    if comando.lower() in key:
      return value(recon)
    
def ouvir(recon):
  print('Fale algo...')
  audio = recon.listen(source)
  print('Reconhecendo...')
  comando = recon.recognize_google(audio, language='pt')
  return comando


recon = sr.Recognizer()
recon.energy_threshold = 50
recon.dynamic_energy_threshold = False
engine = pyttsx3.init()
pygame.mixer.init()
with sr.Microphone() as source:
  recon.adjust_for_ambient_noise(source, duration=3)
  while True:
    try:
      comando = ouvir(recon)
      if 'sexta-feira' in comando:
        falar(detectarPeriodoDoDia()+', mestre. Como posso ajudá-lo?')
        print(comando)
        esperar = input('Pressione Enter para continuar...')
        comando = ouvir(recon)
        mapearComandos(comando, recon)
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
