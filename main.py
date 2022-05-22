from gtts import gTTS
from io import BytesIO
from datetime import datetime
from os.path import exists
import speech_recognition as sr
import pygame
import json
import time

recon = sr.Recognizer()
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
      comando (str): Transcrição do áudio capturado.
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
        
        if exists('carteira.json') == False:
          file = open('carteira.json', 'w')
          cartoes = {
            'cartoes': [
              infoCartao
            ]
          }
          json.dump(cartoes, file)
        else:
          file = open('carteira.json', 'r')
          data = json.load(file)
          data["cartoes"].append(infoCartao)
          file.close()
          file = open('carteira.json', 'w')
          json.dump(data, file)
          file.close()
        falar('O seu cartão foi cadastrado.')
        time.sleep(3)
        break
      
      except sr.UnknownValueError:
        falar('Desculpe, não entendi o que disse.')
        time.sleep(3)
        continue
      
  except IOError:
    raise IOError('Arquivo não encontrado.')

def consultarCartoesCadastrados():
  """
  Consulta todos os cartões cadastrados na carteira.

  Raises:
      IOError: Aciona essa exception caso o arquivo carteira.json não seja encontrado.
  """
  try:
    if exists('carteira.json') == False:
      falar('Não há cartões cadastrados.')
      time.sleep(3)
    else:
      file = open('carteira.json', 'r')
      data = json.load(file)
      if len(data["cartoes"]) < 1:
        falar('Não há cartões cadastrados.')
        time.sleep(3)
      else:  
        falar("Lendo os cartões na sua carteira.")
        time.sleep(3)
        for cartao in data["cartoes"]:
          falar("Cartão "+cartao["numero"]+" com data de validade "+cartao["dataValidade"]+" e código de segurança "+cartao["codigoSeguranca"])
          time.sleep(20)
          
  except IOError:
    raise IOError('Arquivo não encontrado')

def lerHistoricoCompras():
  """
  Lê todo o histórico de compras do usuário.

  Raises:
      IOError: Aciona essa exception caso o arquivo compras.json não seja encontrado.
  """
  try:
    if exists('compras.json') == False:
      falar('Nenhuma compra foi realizada.')
      time.sleep(3)
    else:
      file = open('compras.json', 'r')
      data = json.load(file)
      if len(data["historico"]) < 1:
        falar('Nenhuma compra foi realizada.')
        time.sleep(3)
      else:  
        falar("Lendo seu histórico de compras.")
        time.sleep(3)
        for compra in data["historico"]:
          falar("Compra realizada no dia "
            +compra["dataCompra"]+" às "+compra["horarioCompra"]+" no estabelecimento "
            +compra["estabelecimento"]+" no valor de "+compra["valorCompra"]
            +" utilizando o cartão "+compra["cartaoUtilizado"])
          time.sleep(20)
          
  except IOError:
    raise IOError('Arquivo não encontrado')

def excluirCartao():
  """
  Exclui o cartão desejado da carteira.

  Raises:
      IOError: Aciona essa exception caso o arquivo carteira.json não seja encontrado.
  """
  try:
    if exists('carteira.json') == False:
      falar('Nenhum cartão foi encontrado.')
      time.sleep(3)
    else:
      file = open('carteira.json', 'r')
      data = json.load(file)
      file.close()
      if len(data["cartoes"]) < 1:
        falar('Nenhum cartão foi encontrado.')
        time.sleep(3)
      else:
        falar("Qual o número do cartão que deseja excluir?")
        numeroCartao = ouvir()
        cartaoEncontrado = False
        time.sleep(3)
        for cartao in data["cartoes"]:
          if numeroCartao.replace(" ", "") == cartao["numero"].replace(" ", ""):
            data["cartoes"].remove(cartao)
            falar("Cartão "+numeroCartao+" removido!")
            file = open('carteira.json', 'w')
            json.dump(data, file)
            file.close()
            cartaoEncontrado = True
            time.sleep(20)
        
        if cartaoEncontrado == False:
          falar("Nenhum cartão com esse número foi encontrado.")
          time.sleep(6)
          
  except IOError:
    raise IOError('Arquivo não encontrado')

def mapearComandos(comando):
  """
  Método utilizado para mapear o comando falado pelo o usuário às funções correspondentes.
  Caso encontre o comando, executará a função equivalente.

  Args:
      comando (str): Texto do comando enviado dito pelo o usuário.

  Returns:
      value (function): Retorna a execução da função correspondente com o comando passado.
  """
  comandos = {
    ('abrir histórico de compras', 'ver histórico de compras', 'histórico de compras'): lerHistoricoCompras,
    ('cadastrar novo cartão', 'cadastrar cartão', 'cadastrar cartão de crédito'): cadastrarCartao,
    ('ver cartões cadastrados', 'consultar cartões cadastrados', 'consultar cartões'): consultarCartoesCadastrados,
    ('deletar cartão', 'excluir cartão', 'remover cartão'): excluirCartao
  }
  
  for key, value in comandos.items():
    print(key)
    print(comando.lower())
    if comando.lower() in key:
      return value()

''' 
Passando parâmetros de captura para o reconhecedor de voz.
'''
recon.energy_threshold = 180
recon.dynamic_energy_threshold = False

'''
Inicializando o microfone do SpeechRecognition.
'''
with sr.Microphone() as source:
  recon.adjust_for_ambient_noise(source, duration=3)
  while True:
    try:
      falar('O que deseja fazer?')
      '''
      Ouvir o comando que o usuário deseja executar.
      '''
      comando = ouvir()
      '''
      Passa o comando para a função mapearComandos, que realiza uma busca no dicionário de comandos
      e verifica se aquele comando existe.
      '''
      mapearComandos(comando)
    except sr.UnknownValueError:
      '''
      Exceção gerado caso não reconheça o que foi falado. Por exemplo, ruídos.
      '''
      print('\nTente novamente')
      continue
    except KeyboardInterrupt:
      '''
      Finaliza o programa com interrupção do teclado.
      '''
      print('\nEncerrando...')
      break
    except KeyError:
      '''
      Exceção gerada caso o que foi capturado não esteja de acordo com os comandos existentes.
      '''
      falar('Comando não encontrado.')
      time.sleep(3)
      print('\n Comando não encontrado')
      continue
