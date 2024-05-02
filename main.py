import speech_recognition as sr
import re

def adicionar_pontuacao(texto):
    # Adiciona pontuação após cada frase
    texto_com_pontuacao = re.sub(r'(?<=[.!?]) +', '. ', texto)
    return texto_com_pontuacao

def adicionar_quebras_de_paragrafo(texto):
    # Divide o texto em parágrafos com base em duas quebras de linha
    paragrafos = texto.split('\n\n')
    texto_com_paragrafos = '\n\n'.join(paragrafos)
    return texto_com_paragrafos

def audio_para_texto(arquivo_audio):
    # Inicializa o reconhecedor de voz
    reconhecedor = sr.Recognizer()
    
    # Carrega o arquivo de áudio
    with sr.AudioFile(arquivo_audio) as source:
        # Leitura do áudio
        audio = reconhecedor.record(source)
        
        try:
            # Usa o Google Speech Recognition
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            return texto
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
        except sr.RequestError as e:
            print("Erro no serviço de reconhecimento de fala; {0}".format(e))

# Nome do arquivo de áudio
arquivo_audio = "audio.wav"

# Converte áudio em texto
texto_transcrito = audio_para_texto(arquivo_audio)

# Adiciona pontuação
texto_com_pontuacao = adicionar_pontuacao(texto_transcrito)

# Adiciona quebras de parágrafo
texto_final = adicionar_quebras_de_paragrafo(texto_com_pontuacao)

# Salva o texto em um arquivo .txt
with open("transcricao.txt", "w") as arquivo:
    arquivo.write(texto_final)

print("Transcrição concluída e salva em 'transcricao.txt'")
