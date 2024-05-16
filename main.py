import os
import ast
from datetime import timedelta
import whisper
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import AudioFileClip

# Função para converter segundos em hh:mm:ss
def converter_segundos_para_tempo(segundos):
    """
    Converte segundos em uma string no formato hh:mm:ss.

    :param segundos: Tempo em segundos a ser convertido.
    :return: String representando o tempo no formato hh:mm:ss.
    """
    tempo = str(timedelta(seconds=segundos)).split('.')[0]  # Remove os milissegundos
    return tempo

# Função para salvar as legendas
def save_subtitles(list_of_subtitles, path_to_save):
    """
    Salva a transcrição dos áudios em um único arquivo.

    :param list_of_subtitles: Lista contendo os áudios transcritos pela função transcribe_audio_with_whisper().
    :param path_to_save: Diretório onde estão os arquivos brutos das transcrições.
    :return: None
    """
    try:
        with open(path_to_save, mode='a') as f:
            for subtitle in list_of_subtitles:
                f.write(f"{subtitle}\n")
    except Exception as e:
        print(f"Erro ao salvar legendas: {e}")

# Função para dividir arquivos de áudio
def split_audio_file(path, temp_audio_dir):
    """
    Divide um arquivo de áudio em vários clipes.

    :param path: O caminho do arquivo de áudio que será dividido.
    :param temp_audio_dir: O diretório onde os clipes de áudio temporários serão salvos.
    :return: None
    """
    try:
        audio_clip = AudioFileClip(path)
        duration = audio_clip.duration
        counter = 0
        start = 0
        index = 60
        flag_to_exit = False

        if not os.path.exists(temp_audio_dir):
            os.makedirs(temp_audio_dir)
        else:
            for arquivo in os.listdir(temp_audio_dir):
                caminho_arquivo = os.path.join(temp_audio_dir, arquivo)
                if os.path.isfile(caminho_arquivo):
                    os.remove(caminho_arquivo)
                    print(f'Arquivo {arquivo} excluído.')

        while True:
            audio_clip = AudioFileClip(path)
            if index >= duration:
                flag_to_exit = True
                index = duration
            temp = audio_clip.subclip(start, index)
            temp_saving_location = os.path.join(temp_audio_dir, f'temp_{counter}.mp3')
            temp.write_audiofile(filename=temp_saving_location)
            temp.close()
            counter += 1
            start = index
            audio_clip.close()
            if flag_to_exit:
                break
            index += 60
        print('Arquivo dividido, iniciando processo de transcrição...')
    except Exception as e:
        print(f"Erro ao dividir o arquivo de áudio: {e}")

# Função para transcrever áudio usando Whisper
def transcribe_audio_with_whisper(base_path_to_saved_files, subtitles_path):
    """
    Transcreve áudios em .mp3 utilizando a engine Whisper da OpenAI.
    Acessa a pasta contendo os áudios temporários e gera uma lista com a transcrição dos mesmos.

    :param base_path_to_saved_files: Diretório temporário contendo os áudios a serem transcritos.
    :param subtitles_path: Caminho para o arquivo de legendas.
    :return: None
    """
    try:
        list_of_files = [files for files in os.listdir(base_path_to_saved_files) if files.endswith(".mp3")]

        start = 0
        id_counter = 0
        final_list_of_text = []
        model = whisper.load_model("medium", device='cpu')
        
        for index, file in enumerate(list_of_files):
            path_to_saved_file = os.path.join(base_path_to_saved_files, file)
            audio_clip = AudioFileClip(path_to_saved_file)
            duration = audio_clip.duration
            audio_clip.close()

            out = model.transcribe(path_to_saved_file)
            print(f'{index + 1} of {len(list_of_files)} - OK')

            list_of_text = out['segments']
            for line in list_of_text:
                line['start'] += start
                line['end'] += start
                line['id'] = id_counter
                id_counter += 1

                final_list_of_text.append(line)

            start += duration

        for index, data in enumerate(final_list_of_text[:-1]):
            fur_data = final_list_of_text[index + 1]
            data['end'] = fur_data['start']
            data['duration'] = data['end'] - data['start']

        save_subtitles(list_of_subtitles=final_list_of_text, path_to_save=subtitles_path)
        print('Fim das Transcrições')
    except Exception as e:
        print(f"Erro na transcrição do áudio: {e}")

# Função para processar o arquivo de legendas e formatar em um arquivo amigável
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

# Função para escrever o arquivo formatado
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

def main():
    # Diretórios do projeto
    input_dir = 'input'
    temp_audio_dir = 'temp_audio'
    output_dir = 'output'

    # Criação dos diretórios, se não existirem
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_audio_dir, exist_ok=True)

    # Verificar se há arquivos na pasta 'input'
    input_files = [file for file in os.listdir(input_dir) if file.endswith('.mp4')]
    if not input_files:
        print("O diretório 'input' está vazio.")
        return

    # Iterar sobre todos os arquivos na pasta 'input'
    for file_name in input_files:
        input_file_path = os.path.join(input_dir, file_name)
        base_name = os.path.splitext(file_name)[0]
        temp_subtitle_path = os.path.join(output_dir, f'{base_name}_subtitles.txt')
        final_transcription_path = os.path.join(output_dir, f'{base_name}_transcription.txt')

        # Processamento dos arquivos
        split_audio_file(input_file_path, temp_audio_dir)
        transcribe_audio_with_whisper(temp_audio_dir, temp_subtitle_path)
        textos_com_marcacoes = processar_arquivo_origem(temp_subtitle_path)
        escrever_arquivo_destino(textos_com_marcacoes, final_transcription_path)

        # Limpar o diretório temp_audio
        for temp_file in os.listdir(temp_audio_dir):
            temp_file_path = os.path.join(temp_audio_dir, temp_file)
            os.remove(temp_file_path)

if __name__ == "__main__":
    main()