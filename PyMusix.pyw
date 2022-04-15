#Copyleft Otto Varteva 2022 :)
#Licenced under the GNU GPLv3 licence

# Importing all the necessary modules
from tkinter import *
from tkinter import filedialog
import pygame.mixer as mixer        
import os
import pygame
from sys import platform
import notif
from pathlib import Path


# Initializing the mixer
mixer.init()
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)
pygame.init()
is_stopped = True
def check_event():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
                next_selection()
    root.after(100, check_event)
# Play, Stop, Load and Pause & Resume functions
def play_song(song_name: StringVar, songs_list: Listbox, status: StringVar):
    global is_stopped
    song_name.set(songs_list.get(ACTIVE))

    mixer.music.load(songs_list.get(ACTIVE))
    mixer.music.play()

    status.set("Song PLAYING")
    is_stopped = False
    notif.notify(playlist.get(playlist.curselection()))


def stop_song(status: StringVar):
    global is_stopped
    mixer.music.stop()
    status.set("Song STOPPED")
    is_stopped = True
    print(song_status)


def load(listbox):
    os.chdir(filedialog.askdirectory(title='Open a songs directory'))
    top = os.getcwd()
    tracks = os.listdir()
    listbox.delete(0,'end')
    for root, dirs, filenames in os.walk(top, topdown=False):
        for fl in filenames:
            currentFile=os.path.join(root, fl)
            if currentFile.endswith(".mp3"):
                listbox.insert(END, fl)


def pause_song(status: StringVar):
    global is_stopped
    mixer.music.pause()
    status.set("Song PAUSED")
    is_stopped = True


def resume_song(status: StringVar):
    global is_stopped
    mixer.music.unpause()
    status.set("Song RESUMED")
    is_stopped = False

def next_selection():
    print(song_status)
    print(is_stopped)
    if not is_stopped:
        selection_indices = playlist.curselection()
        next_selection = 0
        if len(selection_indices) > 0:
            last_selection = int(selection_indices[-1])
            playlist.selection_clear(selection_indices)
        if last_selection < playlist.size() - 1:
            next_selection = last_selection + 1
            playlist.activate(next_selection)
            print(playlist.activate(next_selection))
            playlist.selection_set(next_selection)
            play_song(current_song, playlist, song_status)

def kill():
    pygame.mixer.music.stop()
    root.destroy()



# Creating the master GUI
root = Tk()
window = Canvas(root)
root.geometry('700x250')
root.title('PyMusix')
root.resizable(0, 0)
# Titlebar
title_bar = Frame(root,bg='gold', relief='ridge', bd=2)
title_bar.place(y=0)
close_button = Button(title_bar, bg="gold",activebackground="gold", text='X',font=("W95FA",14,"bold"), command=kill, bd=0, highlightthickness=0)
Label(title_bar, text='PyMusix',bg="gold", bd=2, font=('W95FA', 14),).place(x=5, y=0)
window = Canvas(root)


if platform == "linux" or platform == "linux2":
    root.wm_attributes('-type', 'splash')
elif platform == "win32":
    from ctypes import windll

    GWL_EXSTYLE=-20
    WS_EX_APPWINDOW=0x00040000
    WS_EX_TOOLWINDOW=0x00000080

    def set_appwindow(root):
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())

    def main():
        root.wm_title("PyMusix")
        root.overrideredirect(True)
        root.after(10, lambda: set_appwindow(root))
        root.update()

    if __name__ == '__main__':
        main()

# All the frames
song_frame = LabelFrame(root, text='Current Song',font="consolas", bg='Grey',fg="white", width=400, height=80, bd=5)
song_frame.place(x=0, y=30)

button_frame = LabelFrame(root, text='Control Buttons',font="consolas", bg='Grey',fg="white", width=400, height=120,bd=5)
button_frame.place(y=110)

listbox_frame = LabelFrame(root, text='Playlist',font="consolas", bg='grey', fg="white", bd=5)
listbox_frame.place(x=400, y=30, height=200, width=300,)

# All StringVar variables
current_song = StringVar(root, value='<Not selected>')

song_status = StringVar(root, value='<Not Available>')

# Playlist ListBox
playlist = Listbox(listbox_frame, font=('consolas', 11, "bold"), selectbackground='Gold',bg="silver", fg="navyblue")

scroll_bar = Scrollbar(listbox_frame, orient=VERTICAL)

scroll_bar.pack(side=RIGHT, fill=BOTH)

playlist.config(yscrollcommand=scroll_bar.set)

scroll_bar.config(command=playlist.yview)

playlist.pack(fill=BOTH, padx=5, pady=5)

# SongFrame Labels
Label(song_frame, text='CURRENTLY PLAYING:',bg="gray", font=('consolas', 10, 'bold'),).place(x=5, y=20)

song_lbl = Label(song_frame, textvariable=current_song, bg='gray',bd=3, relief="groove",font=("consolas", 12, "bold"), width=25,)

song_lbl.place(x=150, y=17)

# Buttons in the main screen
pause_btn = Button(button_frame, text='Pause',fg="navyblue", bg='gold', font=("consolas", 13,"bold"), width=7,
                    command=lambda: pause_song(song_status))
pause_btn.place(x=15, y=10)

stop_btn = Button(button_frame, text='Stop', fg="navyblue",bg='gold', font=("consolas", 13,"bold"), width=7,
                  command=lambda: stop_song(song_status))
stop_btn.place(x=105, y=10)

play_btn = Button(button_frame, text='Play',fg="navyblue", bg='gold', font=("consolas", 13,"bold"), width=7,
                  command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=195, y=10)

resume_btn = Button(button_frame, text='Resume', fg="navyblue",bg='gold', font=("consolas", 13,"bold"), width=7,
                    command=lambda: resume_song(song_status))
resume_btn.place(x=285, y=10)

load_btn = Button(button_frame, text='Load Directory', fg="navyblue",bg='gold', font=("consolas", 13,"bold"), width=38,
                  command=lambda: load(playlist))
load_btn.place(x=10, y=55)



# Pack
Label(root, textvariable=song_status,fg="navyblue", bg='gray', font=('consolas', 9, "bold"), justify=LEFT).pack(side=BOTTOM, fill=X)
title_bar.pack(expand=1, fill=X)
close_button.pack(side=RIGHT)
window.pack(expand=1, fill=BOTH)

def get_pos(event):
    xwin = root.winfo_x()
    ywin = root.winfo_y()
    startx = event.x_root
    starty = event.y_root
    ywin = ywin - starty
    xwin = xwin - startx

    def move_window(event):
        root.geometry("700x250" + "+{0}+{1}".format(event.x_root + xwin, event.y_root + ywin))
        starty = event.y_root
        startx = event.x_root
    title_bar.bind('<B1-Motion>', move_window)

title_bar.bind("<1>", get_pos)


# Finalizing the GUI
check_event()
root.update()
root.mainloop()
