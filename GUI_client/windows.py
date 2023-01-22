import socket
import tkinter
import customtkinter
from tkinter import filedialog
from tkinter import StringVar
import os
import sys
from PIL import ImageTk, Image
from io import BytesIO

ip_server = ''

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("System")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1280x800")
app.title('Face_search')
app.resizable(False, False)

var = StringVar()
stat = StringVar()

lom = 'Upload a photo to get information about a person.'

stat.set('Server connect 🟢')
var.set(lom)

a = 0

img = ImageTk.PhotoImage(Image.open('banner.png'))
panel = customtkinter.CTkLabel(app, image=img, text='')
panel.place(relx=0.5, rely=0.16, anchor=tkinter.CENTER)


def openfilename():
    global data_id

    # open file dialog box to select image
    # The dialogue box has a title "Open"

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip_server, 9090))
        filename = filedialog.askopenfilename(title='"pen')
        file = open(f'{filename}', mode='rb')
        data = file.read(1024)
        while data:
            client.send(data)
            data = file.read(1024)
            if not data:
                client.send('end'.encode())
        file.close()

        message = client.recv(1024)
        data_id = message.decode('utf-8')
    except:
        error()
    var.set(data_id)
    client.close()


def error():
    stat.set('Server disconnect 🟥')
    data_id = ''
    var.set('')
    if a == 1:
        lbl3 = customtkinter.CTkLabel(
            app, textvariable=stat, font=("Arial Bold", 20))
        lbl3.place(relx=0.09, rely=0.96, anchor=tkinter.CENTER)
        lbl5 = customtkinter.CTkLabel(
            app, text='Version 1.0', font=("Arial Bold", 20))
        lbl5.place(relx=0.99, rely=0.96, anchor=tkinter.SE)
    button = customtkinter.CTkButton(master=app, text="Restart", command=res)
    button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    button1 = customtkinter.CTkButton(master=app, text="Exit", command=ex)
    button1.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    app.mainloop()


def res():
    os.execv(sys.executable, ['python'] + sys.argv)


def ex():
    sys.exit()


try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_server, 9090))
    client.close()

    lbl1 = customtkinter.CTkLabel(
        app, textvariable=stat, font=("Arial Bold", 20))
    lbl1.place(relx=0.08, rely=0.96, anchor=tkinter.CENTER)
    lbl5 = customtkinter.CTkLabel(
        app, text='Version 1.0', font=("Arial Bold", 20))
    lbl5.place(relx=0.95, rely=0.96, anchor=tkinter.CENTER)

    lbl2 = customtkinter.CTkLabel(
        app, text='Id:', textvariable=var, font=("Arial Bold", 20))
    lbl2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # Use CTkButton instead of tkinter Button
    button = customtkinter.CTkButton(
        master=app, text="Upload", command=openfilename, font=("Arial Bold", 25))
    button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

except:
    a = 1
    error()

app.mainloop()
