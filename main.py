from gtts import gTTS
from io import BytesIO
from datetime import datetime
import speech_recognition as sr
import webbrowser as wb
import pygame
import pyttsx3
import linecache

def abrirNavegador(link):
  wb.open_new_tab(link)

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
      input('Aperte enter para ir ao próximo evento.')
      print(line)
    
    f.close()
  except OSError:
    print('Arquivo de agenda não encontrado')

def checarHoras(recon):
  horas = datetime.today().strftime('%H')
  minutos = datetime.today().strftime('%M')
  segundos = datetime.today().strftime('%S')
  falar('Agora são '+horas+' horas e '+minutos+' minutos e '+segundos+' segundos')

def checarPrevisaoTempo(recon):
  falar('De qual cidade?')
  cidade = ouvir(recon)
  falar('Vou mostrar para você a previsão do tempo da cidade de '+cidade)
  abrirNavegador('https://www.google.com/search?q=previsão+do+tempo '+cidade)
  
def classificacaoBrasileirao(recon):
  falar('Vou mostrar para você a tabela do brasileirão série A')
  abrirNavegador('https://www.google.com/search?q=brasileirao%20série%20A#sie=lg;/g/11sfc7_5p3;2;/m/0fnk7q;st;fp;1;;')

def cantarParabens(recon):
  falar('Parabéns pra você, nesta data querida! Muitas felicidades, muitos anos de vida.')  
  
def nomesVingadores(recon):
  return

def mapearComandos(comando, recon):
  comandos = {
    ('ler agenda', 'ver agenda', 'quero ver agenda', 'quero ler minha agenda', 'abrir agenda'): lerAgenda,
    ('cadastrar evento na agenda', 'cadastrar novo evento na agenda', 'cadastrar evento'): cadastrarEventoAgenda,
    ('checar as horas', 'que horas são', 'checar horário'): checarHoras,
    ('checar previsão do tempo', 'como vai estar o tempo hoje', 'como está o clima hoje', 'como está o clima'): checarPrevisaoTempo,
    ('classificação do brasileirão', 'tabela do brasileirão'): classificacaoBrasileirao,
    ('canta parabéns', 'me cante parabéns', 'canta parabéns ai', 'sabe cantar parabéns'): cantarParabens
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


engine = pyttsx3.init()
recon = sr.Recognizer()
recon.energy_threshold = 50
recon.dynamic_energy_threshold = False
pygame.mixer.init()
with sr.Microphone() as source:
  recon.adjust_for_ambient_noise(source, duration=3)
  while True:
    engine.runAndWait()
    try:
      comando = ouvir(recon)
      if 'sexta-feira' in comando:
        falar(detectarPeriodoDoDia()+', mestre. Como posso ajudá-lo?')
        print(comando)
        esperar = input('Pressione Enter para continuar...')
        comando = ouvir(recon)
        mapearComandos(comando, recon)
        print(comando)
        #esperar = input('Pressione Enter para continuar...')
    except sr.UnknownValueError:
      print('\nTente novamente')
      continue
    except KeyboardInterrupt:
      print('\nEncerrando...')
      break
    except KeyError:
      print('\n Comando não encontrado')
      continue
