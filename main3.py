"""
Inspirado no vídeo: https://www.youtube.com/watch?v=E0_kG5j6lEo
"""
import whisper
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import *
import os

path = "audio2.mp4"
base_path_to_saved_files = "/Users/brunoazevedo/MyProjects/Speak_to_text/temp_audio/"
path_to_subtitles = '/Users/brunoazevedo/MyProjects/Speak_to_text/subtitles/subtitles2.txt'

def save_subtitles(list_of_subtitles):
    """
    Salva a trancrição dos áudios em um único arquivo

    :param list_of_subtitles: Lista contendo os áudios transcritos pela função transcribe_audio_with_whisper()
    :param path_to_save: Diretório onde estão os arquivos brutos das trasncrições
    :return: None
    """
    path_to_save = '/Users/brunoazevedo/MyProjects/Speak_to_text/subtitles/subtitles2.txt'
    with open(path_to_save, mode='a+') as f:
        for i in list_of_subtitles:
            f.write("{}\n".format(i))

def split_audio_file(path, diretorio_temp_audio):
    """
    Divide um arquivo de áudio em vários clipes.

    :param path: O caminho do arquivo de áudio que será dividido.
    :param diretorio_temp_audio: O diretório onde os clipes de áudio temporários serão salvos.
    :return: None
    """
    # Importa o arquivo de áudio na variável audio_clip
    audio_clip = AudioFileClip(path) 
    duration = audio_clip.duration
    counter = 0
    start = 0
    audio_clip.close()
    index = 60
    flag_to_exit = False

    if not os.path.exists(diretorio_temp_audio):
        # Se não existir, crie o diretório
        os.makedirs(diretorio_temp_audio)
    else:
        # Se o diretório existir, exclua todos os arquivos dentro dele
        for arquivo in os.listdir(diretorio_temp_audio):
            caminho_arquivo = os.path.join(diretorio_temp_audio, arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
                print(f'Arquivo {arquivo} excluído.')

    while True:
        audio_clip = AudioFileClip(path)
        if index >= duration:
            flag_to_exit = True
            index = duration
        # Garante que o tempo final do sub-clip não ultrapasse a duração total do áudio
        if index > duration:
            index = duration
        temp = audio_clip.subclip(start, index)
        temp_saving_location = os.path.join(diretorio_temp_audio, f'temp_{counter}.mp3')
        temp.write_audiofile(filename=temp_saving_location)
        temp.close()
        counter += 1
        start = index
        audio_clip.close()
        if flag_to_exit:
            break
        index += 60
    print('Arquivo dividido')


def transcribe_audio_with_whisper(base_path_to_saved_files):
    """
    Transcreve áudios em .mp3 utilizando a engine Whisper da OpenAI.
    Acessa a pasta contendo os áudios temporários e gera uma lista com a transcrição dos mesmos.

    :param base_path_to_saved_files: Diretório temporário contendo os áudios a serem transcritos
    :return: None
    """
    # Obtém a lista de arquivos em temp_audio filtrando apenas por arquivos .mp3
    list_of_files = []
    for files in os.listdir(base_path_to_saved_files):
        if files.endswith(".mp3"):
            list_of_files.append(files)

    start = 0
    end = 0
    id_counter = 0

    final_list_of_text = []
    len_list_of_files = len(list_of_files)
    model = whisper.load_model("medium", device='cpu')
    for index in range(len_list_of_files):
        path_to_saved_file = os.path.join(base_path_to_saved_files, f'temp_{index}.mp3')
        audio_clip = AudioFileClip(path_to_saved_file)

        duration = audio_clip.duration
        audio_clip.close()

        out = model.transcribe(path_to_saved_file)
        
        print(f'{index} of {len_list_of_files} - OK')
        
        list_of_text = out['segments']
        for line in list_of_text:
            line['start'] += start
            line['end'] += start
            line['id'] = id_counter
            id_counter += 1

            end = line['end']
            final_list_of_text.append(line)

        start += duration

    for index in range(len(final_list_of_text)):
        data = final_list_of_text[index]
        if index +1 >= len(final_list_of_text):
            break

        fur_data = final_list_of_text[index+1]
        data['end'] = fur_data['start']
        data['duration'] = data['end'] - data['start']

    save_subtitles(list_of_subtitles=final_list_of_text)
    print('Fim das Transcrições')

#split_audio_file(path, base_path_to_saved_files)
transcribe_audio_with_whisper(base_path_to_saved_files)
