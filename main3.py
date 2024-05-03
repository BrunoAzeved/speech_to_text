import whisper
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import *
import os

def save_subtitles(list_of_subtitles):
    path_to_save = '/Users/brunoazevedo/MyProjects/Speak_to_text/subtitles/subtitles0.txt'
    with open(path_to_save, mode='a+') as f:
        for i in list_of_subtitles:
            f.write("{}\n".format(i))

path = "audio0.mp4"
audio_clip = AudioFileClip(path)
n = round(audio_clip.duration)
counter = 0
start = 0
audio_clip.close()

index=60

flag_to_exit = False

# while(True):
#     audio_clip = AudioFileClip(path)
#     if index >= n:
#         flag_to_exit = True
#         index = n

#     temp = audio_clip.subclip(start, index)
#     temp_saving_location = f'/Users/brunoazevedo/MyProjects/Speak_to_text/temp_audio/temp_{counter}.mp3'
#     temp.write_audiofile(filename=temp_saving_location)
#     temp.close()
#     counter += 1
#     start = index
#     audio_clip.close()
#     if flag_to_exit:
#         break
#     index += 60

#     print('stop')

base_path_to_saved_files = "/Users/brunoazevedo/MyProjects/Speak_to_text/temp_audio/"
list_of_files = os.listdir(base_path_to_saved_files)
start = 0
end = 0
id_counter = 0

final_list_of_text = []
for index in range(len(list_of_files)):
    path_to_saved_file = os.path.join(base_path_to_saved_files, f'temp_{index}.mp3')
    audio_clip = AudioFileClip(path_to_saved_file)

    duration = audio_clip.duration
    audio_clip.close()

    model = whisper.load_model("medium", device='cpu')
    out = model.transcribe(path_to_saved_file)
    print(out)
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
print('stop')
