from gtts import gTTS
from io import BytesIO
from datetime import datetime
import speech_recognition as sr
import pygame
import pyttsx3
import random
import json

recon = sr.Recognizer()
recon.energy_threshold = 150
recon.dynamic_energy_threshold = False
pygame.mixer.init()
fraseConfirmacao = ' Essa informação está correta?'

def falar(texto, language='pt'):
  """
  Reproduz o texto para voz.
  
  Args:
  -------
      texto (str): Texto para ser reproduzido.
      language (str, optional): Escolhe a linguagem para ser reproduzido o texto. Valor padrão 'pt'.
  """
  mp3_fo = BytesIO()
  tts = gTTS(texto, lang=language)
  tts.write_to_fp(mp3_fo)
  pygame.mixer.music.load(mp3_fo, 'mp3')
  pygame.mixer.music.play()

def ouvir():
  """
  Ouve o que o usuário falou e transcreve para texto, retornando esse texto.

  Returns:
      comando (str): Áudio capturado por microfone transcrito.
  """
  audio = recon.listen(source)
  print('Reconhecendo...')
  comando = recon.recognize_google(audio, language='pt')
  print(comando)
  return comando

def cadastrarCartao():
  """
  Cadastra um novo cartão.

  Raises:
      IOError: Aciona essa exception caso o arquivo carteira.json não seja encontrado.
  """
  numeroCartao = ''
  dataValidadeCartao = ''
  codigoSegurancaCartao = ''
  confirmacao = ''
  try:
    while True:
      
      try: 
        while True:  
          falar('Por gentileza, fale os 16 dígitos do seu cartão.')
          numeroCartao = ouvir()
          falar('Os 16 dígitos do seu cartão são: '+numeroCartao+fraseConfirmacao)
          confirmacao = ouvir()
          if 'sim' in confirmacao.lower() or 'correto' in confirmacao.lower():
            break
        while True:
          falar('Fale a data de validade do seu cartão.')
          dataValidadeCartao = ouvir()
          falar('A data de validade do seu cartão é '+dataValidadeCartao+fraseConfirmacao)
          confirmacao = ouvir()
          if 'sim' in confirmacao.lower() or 'correto' in confirmacao.lower():
            break
        while True:
          falar('Fale o código de segurança do seu cartão.')
          codigoSegurancaCartao = ouvir()
          falar('O código de segurança do seu cartão é '+codigoSegurancaCartao+fraseConfirmacao)
          confirmacao = ouvir()
          if 'sim' in confirmacao.lower() or 'correto' in confirmacao.lower():
            break
        
        infoCartao = {
          'numero': numeroCartao,
          'dataValidade': dataValidadeCartao,
          'codigoSeguranca': codigoSegurancaCartao
        }
        print(infoCartao)
        falar('O seu cartão foi cadastrado.')
        break
      
      except sr.UnknownValueError:
        falar('Desculpe, não entendi o que disse.')
        continue
      
  except IOError:
    raise IOError('Arquivo não encontrado.')

def consultarCartoesCadastrados():
  # try:
    
  # except IOError:
  #   raise IOError('Arquivo não encontrado')
  return

def lerHistoricoCompras():
  return


def excluirCartao():
  return

  
'''
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
'''

'''
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
'''
  
def mapearComandos(comando):
  comandos = {
    ('cadastrar novo cartão', 'cadastrar cartão', 'cadastrar cartão de crédito'): cadastrarCartao,
    ('ver cartões cadastrados', 'consultar cartões cadastrados', 'consultar cartões'): consultarCartoesCadastrados,
    ('abrir histórico de compras', 'ver histórico de compras', 'histórico de compras'): lerHistoricoCompras,
    ('deletar cartão', 'excluir cartão'): excluirCartao
  }
  
  for key, value in comandos.items():
    if comando.lower() in key:
      return value()

with sr.Microphone() as source:
  recon.adjust_for_ambient_noise(source, duration=3)
  while True:
    try:
      falar('O que deseja fazer?')
      comando = ouvir()
      #esperar = input('Pressione Enter para continuar...')
      mapearComandos(comando)
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
