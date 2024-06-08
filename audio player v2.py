import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import time


pygame.mixer.init()


root = tk.Tk()
root.title("Audio Player")
root.geometry("800x800")



background_image = Image.open(r"C:\Users\karth\Downloads\audioplayer.jpeg") 
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


file_paths = []
current_duration = 0


is_paused = False


def load_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
    listbox.delete(0, tk.END) 
    for file_path in file_paths:
        file_name = file_path.split('/')[-1] 
        listbox.insert(tk.END, file_name)

def get_audio_duration(file_path):
    if file_path.endswith('.mp3'):
        audio = MP3(file_path)
    elif file_path.endswith('.wav'):
        audio = WAVE(file_path)
    else:
        return 0
    return audio.info.length

def play_audio():
    global is_paused, current_duration
    selected_index = listbox.curselection()  
    if selected_index:
        file_path = file_paths[selected_index[0]]  
        current_duration = get_audio_duration(file_path)
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        is_paused = False
        toggle_button.config(text="Pause")
        progress_bar.config(to=current_duration)
        update_progress_bar()

def toggle_pause_unpause():
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        toggle_button.config(text="Pause")
    else:
        pygame.mixer.music.pause()
        toggle_button.config(text="Resume")
    is_paused = not is_paused

def stop_audio():
    pygame.mixer.music.stop()
    progress_bar.set(0)
    toggle_button.config(text="Pause")

def update_progress_bar():
    if pygame.mixer.music.get_busy():
        current_pos = pygame.mixer.music.get_pos() / 1000  
        progress_bar.set(current_pos)
        progress_label.config(text=f"{int(current_pos)} / {int(current_duration)} s")
        root.after(1000, update_progress_bar) 

def play_previous():
    current_index = listbox.curselection()
    if current_index and current_index[0] > 0:
        listbox.select_clear(0, tk.END)
        listbox.select_set(current_index[0] - 1)
        play_audio()

def play_next():
    current_index = listbox.curselection()
    if current_index and current_index[0] < len(file_paths) - 1:
        listbox.select_clear(0, tk.END)
        listbox.select_set(current_index[0] + 1)
        play_audio()


load_button = tk.Button(root, text="Click here to Add files", command=load_files,bg="black", fg="white", font="Prototype")
play_button = tk.Button(root, text="Play", command=play_audio,bg="black", fg="white", font="Prototype")
toggle_button = tk.Button(root, text="Pause", command=toggle_pause_unpause, bg="black", fg="white", font="Prototype")

previous_button = tk.Button(root, text="Previous", command=play_previous,bg="black", fg="white", font="Prototype")
next_button = tk.Button(root, text="Next", command=play_next, bg="black", fg="white", font="Prototype")


listbox = tk.Listbox(root, bg="black", fg="white")


progress_bar = tk.Scale(root, from_=0, to=100, orient="horizontal", length=600, bg="white")
progress_label = tk.Label(root, text="0 | 0 s", bg="white")


load_button.place(x=300, y=50, width=220, height=50)
listbox.place(x=100, y=150, width=600, height=400)
progress_bar.place(x=100, y=570, width=600, height=30)
progress_label.place(x=360, y=630, width=80, height=20)
previous_button.place(x=100, y=680, width=100, height=50)
play_button.place(x=270, y=680, width=100, height=50)
toggle_button.place(x=420, y=680, width=100, height=50)
next_button.place(x=600, y=680, width=100, height=50)




root.mainloop()
