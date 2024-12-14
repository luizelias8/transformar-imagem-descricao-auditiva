import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
from playsound import playsound

# Função para codificar a imagem em Base64
def codificar_imagem(caminho_imagem):
    # Abre o arquivo da imagem no modo binário ('rb') e lê seu conteúdo
    with open(caminho_imagem, 'rb') as imagem:
        # Codifica o conteúdo lido para Base64 e retorna como string UTF-8
        return base64.b64encode(imagem.read()).decode('utf-8')

# Função para gerar a descrição de uma imagem usando o modelo OpenAI
def gerar_descricao_imagem(caminho_imagem, cliente):
    # Codificando a imagem
    imagem_base64 = codificar_imagem(caminho_imagem)

    # Enviando a imagem codificada para o modelo e pedindo para descrever
    resposta = cliente.chat.completions.create(
        model='gpt-4o-mini', # Define o modelo a ser usado
        messages=[{
            'role': 'user', # Especifica que o prompt é do usuário
            'content': [ # Define o conteúdo enviado ao modelo
                {'type': 'text', 'text': 'Descreva o que aparece nesta imagem: '}, # Prompt textual
                {'type': 'image_url', 'image_url': {'url': f'data:image/jpg;base64,{imagem_base64}'}}
            ]
        }],
        max_tokens=500 # Limitar a resposta
    )

    # Retorna a descrição gerada
    return resposta.choices[0].message.content

# Função para gerar o áudio com o modelo TTS-1
def gerar_audio(texto, cliente, arquivo_saida):
    resposta = cliente.audio.speech.create(
        model='tts-1', # Modelo para gerar áudio a partir de texto
        voice='onyx', # Seleção da voz
        input=texto # Texto a ser convertido em fala
    )

    # Salvar o arquivo de áudio em MP3
    resposta.write_to_file(arquivo_saida)

# Função para tocar o áudio
def tocar_audio(caminho_audio):
    """
    Toca o arquivo de áudio especificado.
    """
    try:
        playsound(caminho_audio) # Reproduz o áudio
        print(f"Reproduzindo áudio: {caminho_audio}")
    except Exception as e:
        print(f"Erro ao reproduzir áudio: {e}")

# Caminho para a imagem e o arquivo de áudio
caminho_imagem = 'imagem.jpg'
caminho_arquivo_audio = 'fala.mp3'

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o cliente da API do OpenAI
cliente = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Gerar a descrição da imagem
descricao_imagem = gerar_descricao_imagem(caminho_imagem, cliente)
print("Descrição da imagem:", descricao_imagem)

# Gerar áudio a partir da descrição da imagem
gerar_audio(descricao_imagem, cliente, caminho_arquivo_audio)
print(f"Áudio gerado e salvo em {caminho_arquivo_audio}")

# Toca o áudio
tocar_audio(caminho_arquivo_audio)