import os
import shutil
from datetime import timedelta
import whisper
from moviepy.editor import AudioFileClip
from tqdm import tqdm

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
        with open(path_to_save, mode='w') as f:
            for subtitle in list_of_subtitles:
                f.write(f"{subtitle}\n")
    except Exception as e:
        print(f"Erro ao salvar legendas: {e}")

def split_audio_file(path, temp_audio_dir):
    """
    Divide um arquivo de áudio em vários clipes.

    :param path: O caminho do arquivo de áudio que será dividido.
    :param temp_audio_dir: O diretório onde os clipes de áudio temporários serão salvos.
    :return: None
    """
    try:
        with AudioFileClip(path) as audio_clip:
            duration = audio_clip.duration
            num_clips = int(duration / 60) + (1 if duration % 60 != 0 else 0)
            pbar = tqdm(total=num_clips, desc='Criando arquivos temporários')
            for i in range(num_clips):
                start = i * 60
                end = min((i + 1) * 60, duration)
                temp_saving_location = os.path.join(temp_audio_dir, f'temp_{i}.mp3')
                audio_clip.subclip(start, end).write_audiofile(temp_saving_location, logger=None)
                #print(f'Saved {temp_saving_location}')
                pbar.update(1)  # Atualiza a barra de progresso
            pbar.close()  # Fecha a barra de progresso após completar
    except Exception as e:
        print(f"Erro ao dividir o arquivo de áudio: {e}")

# Função para transcrever áudio usando Whisper
def transcribe_audio_with_whisper(base_path_to_saved_files, output_file):
    """
    Transcreve áudios em .mp3 utilizando a engine Whisper da OpenAI.
    Acessa a pasta contendo os áudios temporários e gera uma lista com a transcrição dos mesmos.

    :param base_path_to_saved_files: Diretório temporário contendo os áudios a serem transcritos.
    :param subtitles_path: Caminho para o arquivo de legendas.
    :return: None
    """
    model = whisper.load_model("tiny", device='cpu')
    final_transcription = []

    files = sorted(os.listdir(base_path_to_saved_files))
    for file in tqdm(files, desc='Transcrevendo áudios'):
        path = os.path.join(base_path_to_saved_files, file)
        result = model.transcribe(path)
        transcription = result['text']
        final_transcription.append(transcription)
    
    save_subtitles(final_transcription, output_file)

def main(input_file, output_folder):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    temp_audio_dir = os.path.join(output_folder, 'temp')
    transcription_path = os.path.join(output_folder, f'{base_name}_transcrito.txt')

    os.makedirs(temp_audio_dir, exist_ok=True)
    split_audio_file(input_file, temp_audio_dir)
    transcribe_audio_with_whisper(temp_audio_dir, transcription_path)
    shutil.rmtree(temp_audio_dir)
    print("Transcriçãoa completa e diretório temporário removido.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_folder = sys.argv[2]
        main(input_file, output_folder)
    else:
        print("Por favor, forneça o caminho do arquivo de entrada e o diretório de saída.")