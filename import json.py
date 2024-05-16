import ast
from datetime import timedelta

def converter_segundos_para_tempo(segundos):
    """
    Converte segundos em uma string no formato hh:mm:ss.

    :param segundos: Tempo em segundos a ser convertido.
    :return: String representando o tempo no formato hh:mm:ss.
    """
    tempo = str(timedelta(seconds=segundos)).split('.')[0]  # Remove os milissegundos
    return tempo

def processar_arquivo_origem(caminho_arquivo_origem):
    """
    Lê o arquivo de origem e retorna uma lista de textos com marcações de tempo.

    :param caminho_arquivo_origem: Caminho para o arquivo de origem.
    :return: Lista de strings com marcações de tempo e texto.
    """
    try:
        with open(caminho_arquivo_origem, 'r') as arquivo_origem:
            linhas = arquivo_origem.readlines()

        textos_com_marcacoes = []
        for linha in linhas:
            try:
                linha_dict = ast.literal_eval(linha)
                inicio_segundos = linha_dict['start']
                fim_segundos = linha_dict['end']
                inicio_tempo = converter_segundos_para_tempo(inicio_segundos)
                fim_tempo = converter_segundos_para_tempo(fim_segundos)
                texto = linha_dict['text']
                texto_com_marcacoes = f"[Início: {inicio_tempo} -> Fim: {fim_tempo}] Texto: {texto}"
                textos_com_marcacoes.append(texto_com_marcacoes)
            except (SyntaxError, ValueError, KeyError) as e:
                print(f"Erro ao processar linha: {e}")
                continue
        return textos_com_marcacoes
    except FileNotFoundError:
        print(f"Arquivo {caminho_arquivo_origem} não encontrado.")
        return []
    except IOError as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo_origem}: {e}")
        return []

def escrever_arquivo_destino(textos_com_marcacoes, caminho_arquivo_destino):
    """
    Escreve os textos com marcações de tempo em um novo arquivo.

    :param textos_com_marcacoes: Lista de strings com marcações de tempo e texto.
    :param caminho_arquivo_destino: Caminho para o arquivo de destino.
    :return: None
    """
    try:
        with open(caminho_arquivo_destino, 'w') as arquivo_destino:
            for texto_com_marcacoes in textos_com_marcacoes:
                arquivo_destino.write(f"{texto_com_marcacoes}\n")
    except IOError as e:
        print(f"Erro ao escrever no arquivo {caminho_arquivo_destino}: {e}")

# Caminhos dos arquivos
caminho_arquivo_origem = 'subtitles/subtitles2_teste.txt'
caminho_arquivo_destino = 'transcricao_audio2_teste.txt'

# Processar e escrever os arquivos
textos_com_marcacoes = processar_arquivo_origem(caminho_arquivo_origem)
if textos_com_marcacoes:
    escrever_arquivo_destino(textos_com_marcacoes, caminho_arquivo_destino)