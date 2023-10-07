from tkinter import *
import tkinter as tk
import player

#fuction to open second window
def goto():
    player.open(root2)

root2 = tk.Tk()
root2.title("MP3 Player")
root2.geometry("500x450")
root2.configure(bg="#451952")
#root.resizable(False,False) #window is resizable or not

my_image = PhotoImage(file="Button Images/mp3logo.png")
image_label=Label(image=my_image,bd=0)
image_label.pack(pady=30)

title_label=Label(text="MP3 PLAYER",bg="#451952",fg="#F39F5A",font=('Helvetica',30,'bold'))
title_label.pack()

Button(root2,text="Let's Music",width=10,height=1,font=("arial",20,"bold"),bd=1,fg="#FFFFFF",bg="#FF6969",command=goto).place(x=160,y=350)

root2.mainloop()
