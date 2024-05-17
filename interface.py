import tkinter as tk
from tkinter import filedialog, ttk
import main

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.mp4")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

def choose_output_folder():
    folder_path = filedialog.askdirectory()
    entry_output.delete(0, tk.END)
    entry_output.insert(0, folder_path)

def transcribe():
    input_file = entry_file.get()
    output_folder = entry_output.get()
    if input_file and output_folder:
        progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='indeterminate')
        progress.grid(row=4, column=1, pady=20)
        progress.start(10)
        main.main(input_file, output_folder)
        progress.stop()
        progress.grid_forget()
        label_status.config(text="Transcription Completed Successfully!")
    else:
        label_status.config(text="Please select an audio file and output folder.")

root = tk.Tk()
root.title("Transcrição de Áudio")

tk.Label(root, text="Selecione o arquivo de áudio:").grid(row=0, column=0, padx=10, pady=10)
entry_file = tk.Entry(root, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=choose_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Selecione o diretório de saída:").grid(row=1, column=0, padx=10, pady=10)
entry_output = tk.Entry(root, width=50)
entry_output.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=choose_output_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Transcribe", command=transcribe, height=2, width=20).grid(row=2, column=1, padx=10, pady=10)

label_status = tk.Label(root, text="")
label_status.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()