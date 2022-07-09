import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from pygame import mixer


class Player():
    def __init__(self) -> None:
        self.IS_PLAYING = False
        self.curr_song_index = 0

    def _get_curr_song_index(self):
        return 0 if len(playlist.curselection())==0 else playlist.curselection()[0]

    def _set_song(self, curr_song_index):
        playlist.activate(curr_song_index)
        playlist.selection_set(curr_song_index)  

    def prev(self):
        curr_song_index = self._get_curr_song_index()
        if curr_song_index > 0:
            playlist.selection_clear(curr_song_index)
            self._set_song(curr_song_index - 1)
            self.play()   

    def next(self):
        curr_song_index = self._get_curr_song_index()
        print(curr_song_index, playlist.size())
        if curr_song_index < playlist.size()-1:
            playlist.selection_clear(curr_song_index)
            self._set_song(curr_song_index + 1)
            self.play()    
    
    def double_clicked(self, event):
        self.play()
    
    def play_or_pause(self):
        self.IS_PLAYING = not self.IS_PLAYING
        if self.IS_PLAYING:
            self.pause()
            btn_text.set("  play  ")
        else:
            self.resume()
            btn_text.set("pause")

    def play(self):
        # print("End_event", mixer.music.get_endevent())
        if playlist.curselection() == ():
            self._set_song(0)
        curr_song = playlist.get(ACTIVE)

        mixer.music.load(curr_song)
        mixer.music.play()

    def pause(self):
        mixer.music.pause()

    def resume(self):
        mixer.music.unpause()

    def lower_vol(self):
        current_vol = mixer.music.get_volume()
        if current_vol > 0:
            mixer.music.set_volume(current_vol - 0.1)

    def increase_vol(self):
        current_vol = mixer.music.get_volume()
        if current_vol < 1:
            mixer.music.set_volume(current_vol + 0.1)
    
    def get_songs(self, selected_folder=None):
        os.chdir(selected_folder)
        songs = os.listdir()

        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert(END, song)

window = Tk()
window.title("Ilgor's Music Player")

frame = Frame(window)

playlist = Listbox(window, height=6, selectmode='extended')
playlist.pack(padx=10, pady=10, fill=BOTH, expand=True) 

player = Player() 
player.get_songs(selected_folder=filedialog.askdirectory())

playlist.bind('<Double-1>', player.double_clicked)

btn_text = StringVar()
btn_text.set("pause")

Button(frame, text="<", command=player.prev).grid(row=1, column=1)
Button(frame, textvariable=btn_text, command=player.play_or_pause).grid(row=1, column=2)
Button(frame, text=">", command=player.next).grid(row=1, column=3)
Button(frame, text="-", command=player.lower_vol).grid(row=1, column=4)
Button(frame, text="+", command=player.increase_vol).grid(row=1, column=5)

frame.pack(expand=True)

mixer.init()
# mixer.music.set_endevent()

player.play()
mainloop()