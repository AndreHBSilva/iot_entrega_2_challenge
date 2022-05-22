from gtts import gTTS
from io import BytesIO
from datetime import datetime
from os.path import exists
import speech_recognition as sr
import pygame
import json
import time
import cv2
import sys

#este é o classificador provido pelo OpenCV, para detectar rostos
classificadorFace = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

'''Aqui existem uma serie de imagens, com diferentes graus de complexidade para testes..'''
#imgPath = './images/Rostos.jpg'
#imgPath = './images/testeDeFogo3.jpg'
#imgPath = './images/testeDeFogo4.jpg'
#imgPath = './images/negativa.jpg'
imgPath = './images/testeDeFogo2.jpg'

#este metodo lê a imagem que passamos na variavel acima, que recebeu o endereço da imagem
img = cv2.imread(imgPath)

''' Adotamos uma metodologia antiga com o Haar Cascade, onde ele detecta as bordas e linhas 
da imagem, porém apenas em escala de CINZA, de acordo com o banco de dados de imagens que consta
no xml, esta metodologia de classificação é anterior ao Deep Learning.'''

#aqui convertemos nossa imagem colorida para tons de cinza.
imagemCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#este algoritmo identifica as faces na imagem que foi informada para detecção multi escalar,
#seguindo as regras do classificador informado no inicio do codigo.
rostos = classificadorFace.detectMultiScale(imagemCinza)
'''
Aqui é desenhado um quadrado onde cada rosto foi identificado na imagem com as propriedades abaixo:
(0,255,0) é a cor do retangulo (AZUL)
2 é a grossura da linha
l é a largura do quadrado da face
a é a altura
x é o ponto inicial no eixo horizontal
y é o ponto inicial no eixo vertical'''
for (x,y,l,a) in rostos:
    img = cv2.rectangle(img, (x,y), (x+l, y+a), (255,0, 0),1)

'''------------------------------------------------------------
  MÉTODOS PARA DETECÇÃO E SINTETIZAÇÃO DE VOZ.
'''

'''Inicializando o reconhecedor de voz.'''
recon = sr.Recognizer()

'''Inicializando o mixer que irá reproduzir os áudios sintetizados.'''
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
  
def encerrar():
  """
  Comando para encerrar/terminar aplicação.
  """
  falar('Encerrando aplicação. Até logo!')
  time.sleep(5)
  sys.exit()

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
    ('cadastrar novo cartão', 'cadastrar meu cartão', 'cadastrar cartão', 'cadastrar cartão de crédito'): cadastrarCartao,
    ('ver cartões cadastrados', 'consultar cartões cadastrados', 'consultar cartões'): consultarCartoesCadastrados,
    ('deletar cartão', 'excluir cartão', 'remover cartão'): excluirCartao,
    ('encerrar', 'sair da aplicação', 'encerrar aplicação', 'fechar aplicação'): encerrar
  }
  
  for key, value in comandos.items():
    if comando.lower() in key:
      return value()

''' 
Passando parâmetros de captura para o reconhecedor de voz.
'''
recon.energy_threshold = 180
recon.dynamic_energy_threshold = False

'''
Inicializando o microfone do SpeechRecognition.
A partir deste momento, se o algoritmo identificar que existe um rosto humano identificado, ele 
prossegue para o assistente de voz.
'''
if len(rostos) > 0:
  cv2.imshow("Faces detectadas", img)
  print('Rosto detectado!')
  print('Pressione qualquer tecla para continuar...')
  cv2.waitKey(0)
  cv2.destroyAllWindows()
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
