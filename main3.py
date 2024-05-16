"""
Inspirado no vídeo: https://www.youtube.com/watch?v=E0_kG5j6lEo
"""
import whisper
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import *
import os

path = "audio2.mp4"
base_path_to_saved_files = "/Users/brunoazevedo/MyProjects/Speak_to_text/temp_audio/"
path_to_subtitles = '/Users/brunoazevedo/MyProjects/Speak_to_text/subtitles/subtitles2_teste.txt'

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
        print('Arquivo dividido')
    except Exception as e:
        print(f"Erro ao dividir o arquivo de áudio: {e}")

def transcribe_audio_with_whisper(base_path_to_saved_files):
    """
    Transcreve áudios em .mp3 utilizando a engine Whisper da OpenAI.
    Acessa a pasta contendo os áudios temporários e gera uma lista com a transcrição dos mesmos.

    :param base_path_to_saved_files: Diretório temporário contendo os áudios a serem transcritos.
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

        save_subtitles(list_of_subtitles=final_list_of_text, path_to_save=path_to_subtitles)
        print('Fim das Transcrições')
    except Exception as e:
        print(f"Erro na transcrição do áudio: {e}")

#split_audio_file(path, base_path_to_saved_files)
transcribe_audio_with_whisper(base_path_to_saved_files)