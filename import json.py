import ast
from datetime import timedelta

# Função para converter segundos em hh:mm:ss
def converter_segundos_para_tempo(segundos):
    tempo = str(timedelta(seconds=segundos)).split('.')[0]  # Remove os milissegundos
    return tempo

# Abrir o arquivo original
with open('subtitles/subtitles0.txt', 'r') as arquivo_origem:
    linhas = arquivo_origem.readlines()

# Extrair o campo 'text' e as marcações de início e fim de cada linha e consolidar em uma lista
textos_com_marcacoes = []
for linha in linhas:
    try:
        # Avaliar a linha como um dicionário Python
        linha_dict = ast.literal_eval(linha)
        # Extrair as marcações de início e fim e o campo 'text'
        inicio_segundos = linha_dict['start']
        fim_segundos = linha_dict['end']
        # Converter segundos para o formato hh:mm:ss
        inicio_tempo = converter_segundos_para_tempo(inicio_segundos)
        fim_tempo = converter_segundos_para_tempo(fim_segundos)
        texto = linha_dict['text']
        # Adicionar as marcações e o texto à lista
        texto_com_marcacoes = f"[Início: {inicio_tempo} -> Fim: {fim_tempo}] Texto: {texto}"
        textos_com_marcacoes.append(texto_com_marcacoes)
    except (SyntaxError, ValueError, KeyError):
        # Se ocorrer um erro ao avaliar a linha ou ao acessar as chaves, continue para a próxima linha
        continue

# Escrever os textos com marcações consolidados em um novo arquivo
with open('textos_com_marcacoes.txt', 'w') as arquivo_destino:
    for texto_com_marcacoes in textos_com_marcacoes:
        arquivo_destino.write(texto_com_marcacoes + '\n')
