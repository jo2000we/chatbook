# main.py
import shutil
import threading
#import time

#import openai

from videoplayer import VideoPlayer
#import recorder
#import multiprocessing

import tkinter as tk
from gpt import initiate, ask
from d_id import generate_video

import queue
import requests

from tkinter import filedialog

def start_chat():
    # Check if a file is selected, if not, get the value from the entry field

    did_keys = []

    if file_path.get():
        # Create an empty list to store the lines

        did_keys = []

        # Open the file in read mode
        with open(file_path.get(), 'r') as file:
            # Loop through each line in the file
            for line in file.readlines():
                # Add the line to the list
                did_keys.append(line.strip())

        # Print the list
        print("Keys wurden eingelesen: ")
        for key in did_keys:
            print(key)

    else:

        did_keys.append(api_did_key_entry.get())

    # Save the entered information
    initiate(info=[api_gpt_key_entry.get(), did_keys, character_entry.get(), information_text.get('1.0', 'end-1c')])

    #Setup welcome video
    print("Starte Kopieren der Animation von Pfad: " + movie_file_path.get())
    shutil.copy2(movie_file_path.get(), 'triggered_video.mp4')  # copy2 bewahrt die ursprünglichen Metadaten der Datei
    print("Kopieren der Animation abgeschlossen!")

    # Close the window
    root.destroy()

def select_file():
    filename = filedialog.askopenfilename()
    if filename:
        file_path.set(filename)
        api_did_key_entry.delete(0, 'end')
        api_did_key_entry.config(state='disabled')
    else:
        api_did_key_entry.config(state='normal')


def select_movie_file():
    filename = filedialog.askopenfilename()
    if filename:
        movie_file_path.set(filename)



root = tk.Tk()
root.title('Konfiguration')

# GPT API Key field
tk.Label(root, text='GPT API Key:').pack()
api_gpt_key_entry = tk.Entry(root)
api_gpt_key_entry.pack()

# D-ID API Key field and file selection
key_file_frame = tk.Frame(root)
key_file_frame.pack()
tk.Label(key_file_frame, text='D-ID API Key oder wähle keys.txt:').pack()
api_did_key_entry = tk.Entry(key_file_frame)
api_did_key_entry.pack(side='left')
file_path = tk.StringVar()
tk.Button(key_file_frame, text='Browse', command=select_file).pack(side='left')

# Movie file field and file selection
movie_file_frame = tk.Frame(root)
movie_file_frame.pack()
tk.Label(movie_file_frame, text='Wähle intro.mp4 aus:').pack()
movie_file_path = tk.StringVar()
tk.Entry(movie_file_frame, textvariable=movie_file_path).pack(side='left')
tk.Button(movie_file_frame, text='Browse', command=select_movie_file).pack(side='left')

# Character field
tk.Label(root, text='Character:').pack()
character_entry = tk.Entry(root)
character_entry.pack()

# Information field
tk.Label(root, text='Information:').pack()
information_text = tk.Text(root)
information_text.pack()

# Start Chat button
tk.Button(root, text='Start Chat', command=start_chat).pack()

root.mainloop()



# Chat GUI
# main.py

def run_videoplayer():
    player = VideoPlayer.get_instance()
    player.initiate_talkinterface()

#video_process = multiprocessing.Process(target=video_player_process)
#video_process.start()
#video_process.join()

player_thread = threading.Thread(target=run_videoplayer)
player_thread.start()


def trigger_video():
    print("Setze Event zum abspielen der Animation")
    player = VideoPlayer.get_instance()
    player.change_event.set()


#UI Textfenster

def handle_enter(event):
    text = text_field.get()
    q.put(text)
    text_field.delete(0, 'end')

def question():
    while True:
        content = q.get()
        print("Frage: " + content)
        url = generate_video(ask(content))
        if url is not None:
            print("Starte Download von Animation, url: " + url)
            video = requests.get(url)
            open('triggered_video.mp4', 'wb').write(video.content)
            print("Download von Animation abgeschlossen!")
            trigger_video()


root = tk.Tk()

text_field = tk.Entry(root)
text_field.bind('<Return>', handle_enter)
text_field.pack()

q = queue.Queue()
t = threading.Thread(target=question)
t.start()

if movie_file_path.get() is not None:
    trigger_video()

def check_queue():
    while not q.empty():
        text = q.get()
    root.after(100, check_queue)

root.after(100, check_queue)
root.mainloop()



#initiate_userinterface()
