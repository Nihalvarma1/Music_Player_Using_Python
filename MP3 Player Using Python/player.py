from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from tkinter import font
import tkinter as tk

#reference from first window(root2) to open this window(root)
def open(root2):
    root=tk.Toplevel(root2)
    #root = Tk()
    root.title("MP3 Player")
    root.geometry("500x450")
    root.configure(bg="#451952")


    #Initialize Pygame Mixer
    pygame.mixer.init()

    #Grab song length time info
    def play_time():
        #check for double timing
        if stopped:
            return
        #grab current song elapsed time
        current_time=pygame.mixer.music.get_pos()/1000
        #throw up temp label to get data
        #slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')
        #convert time format
        converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))

        #Get the Current song tuple number
        current_one = song_box.curselection()
        #grab song title from playlist
        song =song_box.get(ACTIVE)
        #add directory structure and mp3 to the song title
        song = f'C:/Users/Nihal Varma/Desktop/MP3 Player Using Python/Songs/{song}.mp3'

        #get song length with mutagen
        song_mut=MP3(song)
        #get song length
        global song_length
        song_length=song_mut.info.length
        #convert to time format
        converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))

        #increase current time by one second
        current_time+=1
        
        if int(my_slider.get())==int(song_length):
            status_bar.config(text=f'Time Elapsed : {converted_song_length}  of  {converted_song_length}  ')
        elif paused:
            pass
        elif int(my_slider.get())== int(current_time):
            #update slider to position
            slider_position = int(song_length)
            my_slider.config(to=slider_position,value=int(current_time))
        else:
            #update slider to position
            slider_position = int(song_length)
            my_slider.config(to=slider_position,value=int(my_slider.get()))

            #convert time format
            converted_current_time=time.strftime('%M:%S',time.gmtime(int(my_slider.get())))
        
            #output the time to status bar
            status_bar.config(text=f'Time Elapsed : {converted_current_time}  of  {converted_song_length}  ')

            #move this thing along by one second
            next_time =int(my_slider.get())+1
            my_slider.config(value=next_time )

        #output the time to status bar
        #status_bar.config(text=f'Time Elapsed : {converted_current_time}  of  {converted_song_length}  ')
        #update slider position value to current song position
        #my_slider.config(value=int(current_time))
        
        #update time
        status_bar.after(1000,play_time)

    #add song function
    def add_song():
        song = filedialog.askopenfilename(initialdir='audio/',title="Choose a Song",filetypes=(("mp3 Files","*.mp3"),))

        #strip out the directory info and .mp3 from the song name
        song = song.replace("C:/Users/Nihal Varma/Desktop/MP3 Player Using Python/Songs/","")
        song = song.replace(".mp3","")
        
        #add song to list box
        song_box.insert(END, song)

    #add many songs to playlist
    def add_many_songs():
        songs = filedialog.askopenfilenames(initialdir='Songs/audio/',title="Choose a Song",filetypes=(("mp3 Files","*.mp3"),))
        #remove directory and .mp3 for all songs through loop
        for song in songs:
            song = song.replace("C:/Users/Nihal Varma/Desktop/MP3 Player Using Python/Songs/","")
            song = song.replace(".mp3","")
            #add songs to list box
            song_box.insert(END, song)
            
    #play selected song
    def play():
        #set stopped variable to false so song can play
        global stopped
        stopped = False
        song = song_box.get(ACTIVE)
        song = f'C:/Users/Nihal Varma/Desktop/MP3 Player Using Python/Songs/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        #call the playtime function to get song length
        play_time()

        #update slider to position
        #slider_position = int(song_length)
        #my_slider.config(to=slider_position,value=0)

        #Get Current Volume
        #current_volume=pygame.mixer.music.get_volume()
        #slider_label.config(text=current_volume*100)
        
    #create global pause variable
    global paused
    paused=False

    #pause and unpause song
    def pause(is_paused):
        global paused
        paused=is_paused
        if paused:
            #unpause
            pygame.mixer.music.unpause()
            paused=False
        else:
            #pause
            pygame.mixer.music.pause()
            paused=True

    #stop currently playing song
    global stopped
    stopped =False
    def stop():
        #reset slider and status bar
        status_bar.config(text='')
        my_slider.config(value=0)
        #stop song from playing
        pygame.mixer.music.stop()
        song_box.selection_clear(ACTIVE)

        #clear status bar
        status_bar.config(text='')

        #set stop variable to true
        global stopped
        stopped =True

    #Play Next song Using Forward Button
    def next_song():
        #reset slider and status bar
        status_bar.config(text='')
        my_slider.config(value=0)
        #Get the Current song tuple number
        next_one = song_box.curselection()
        #add one to the current song number
        next_one = next_one[0]+1
        #comes to first song is next_one excceds no of songs
        if(next_one>=song_box.size()):
            next_one=0
        #grab song title from playlist
        song =song_box.get(next_one)
        #add directory structure and mp3 to the song title
        song = f'C:/Users/Nihal Varma/Desktop/MP3 Player Using Python/Songs/{song}.mp3'
        #load and play song
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #clear active song bar in playlist listbox
        song_box.selection_clear(0,END)
        #activate new song bar
        song_box.activate(next_one)
        #set active bar to next song
        song_box.selection_set(next_one,last=None)

    #Play previous song in playlist
    def previous_song():
        #reset slider and status bar
        status_bar.config(text='')
        my_slider.config(value=0)
        #Get the Current song tuple number
        prev_one = song_box.curselection()
        #subtract one to the current song number
        prev_one = prev_one[0]-1
        #comes to last song is prev_one is negative
        if(prev_one<0):
            prev_one=song_box.size()-1
        #grab song title from playlist
        song =song_box.get(prev_one)
        #add directory structure and mp3 to the song title
        song = f'C:/Users/Nihal Varma/Desktop/MP3 Player Using Python/Songs/{song}.mp3'
        #load and play song
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #clear active song bar in playlist listbox
        song_box.selection_clear(0,END)
        #activate new song bar
        song_box.activate(prev_one)
        #set active bar to previous song
        song_box.selection_set(prev_one,last=None)

    #Delete a song
    def delete_song():
        stop()
        #delete currently selected song
        song_box.delete(ANCHOR)
        #stop music if it's playing
        pygame.mixer.music.stop()

    #Delete all songs from playlist
    def delete_all_songs():
        stop()
        #deleet all songs
        song_box.delete(0,END)
        #stop music if it's playing
        pygame.mixer.music.stop()

    #Create slider function
    def slide(x):
        #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
        song = song_box.get(ACTIVE)
        song = f'C:/Users/Nihal Varma/Desktop/MP3 Player Using Python/Songs/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0,start=int(my_slider.get()))

    #create volume function
    def volume(x):
        pygame.mixer.music.set_volume(volume_slider.get())
        #get current volume
        #current_volume=pygame.mixer.music.get_volume()
        #slider_label.config(text=current_volume*100)

    #create master frame
    master_frame=Frame(root)
    master_frame.configure(bg="#451952")
    master_frame.pack(pady=20)

    #Create a Playlist Box
    bolded = font.Font(family='Helvetica',weight='bold',size=8) 
    song_box = Listbox(master_frame,bg="#662549",fg="white",width=60,selectbackground="#F39F5A",selectforeground="#070A52",font=bolded)

    song_box.grid(row=0,column=0)
    #Define Player Control Button Images
    back_btn_img =PhotoImage(file='Button Images/backward.png')
    forward_btn_img =PhotoImage(file='Button Images/forward.png')
    play_btn_img =PhotoImage(file='Button Images/play.png')
    pause_btn_img =PhotoImage(file='Button Images/pause.png')
    stop_btn_img =PhotoImage(file='Button Images/stop.png')

    #Create Player Control Frame
    controls_frame=Frame(master_frame)
    controls_frame.configure(bg="#451952")
    controls_frame.grid(row=1,column=0,pady=20)

    #create volume label frame
    volume_frame = LabelFrame(master_frame,text="Volume",bd=0)
    volume_frame.grid(row=0,column=1,padx=20)

    #Create Player Control Button
    back_btn = Button(controls_frame,image=back_btn_img,borderwidth=0,command=previous_song)
    forward_btn = Button(controls_frame,image=forward_btn_img,borderwidth=0,command=next_song)
    play_btn = Button(controls_frame,image=play_btn_img,borderwidth=0,command=play)
    pause_btn = Button(controls_frame,image=pause_btn_img,borderwidth=0,command=lambda: pause(paused))
    stop_btn = Button(controls_frame,image=stop_btn_img,borderwidth=0,command=stop)

    back_btn.grid(row=0,column=0,padx=10)
    forward_btn.grid(row=0,column=1,padx=10)
    play_btn.grid(row=0,column=2,padx=10)
    pause_btn.grid(row=0,column=3,padx=10)
    stop_btn.grid(row=0,column=4,padx=10)

    menu_bolded = font.Font(family='Helvetica',weight='bold',size=10)

    #Create Menu
    my_menu = Menu(root,background="blue", fg="white",font=menu_bolded)
    root.config(menu=my_menu)

    #add song menu
    add_song_menu = Menu(my_menu,background="#662549",fg='#F39F5A',font=menu_bolded)
    my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
    add_song_menu.add_command(label="Add one Song To Playlist",command=add_song)
    add_song_menu.add_command(label="Add Many Songs To Playlist",command=add_many_songs)

    #create delete song menu
    remove_song_menu = Menu(my_menu,background="#662549",fg='#F39F5A',font=menu_bolded)
    my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
    remove_song_menu.add_command(label="Delete A Song From Playlist",command=delete_song)
    remove_song_menu.add_command(label="Delete All Songs From Playlist",command=delete_all_songs)

    #Create Status Bar
    status_bolded = font.Font(family='Helvetica',weight='bold',size=10) 
    status_bar = Label(root,text='',bd=1,relief=GROOVE,anchor=E,fg="#070A52",bg="#F39F5A",font=status_bolded)
    status_bar.pack(fill=X,side=BOTTOM,ipady=2)

    #create music position slider
    my_slider = ttk.Scale(master_frame,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
    #my_slider.config(background='black', fg='grey', troughcolor='#73B5FA', activebackground='#1065BF')
    my_slider.grid(row=2,column=0,pady=10)

    #create volume slider
    volume_slider = ttk.Scale(volume_frame,from_=1,to=0,orient=VERTICAL,value=1,command=volume,length=125)
    volume_slider.pack(pady=10)

    #create temporary slider label
    #slider_label = Label(root,text="0")
    #slider_label.pack(pady=10)

    root.mainloop()

#open()
