import socket
import tkinter
import customtkinter
from tkinter import filedialog
from tkinter import StringVar
import os
import sys
from PIL import ImageTk, Image
from io import BytesIO
import threading
import ssl

ip_server = '' #Server address

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("System")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1280x800")
app.title('Face_search')
app.resizable(False, False)

text_centor = StringVar()
status_server = StringVar()

greetings = 'Upload a photo to get information about a person.'

status_server.set('Server connect 🟢')
text_centor.set(greetings)

trigger_value = 0

img = ImageTk.PhotoImage(Image.open('banner.png'))
panel = customtkinter.CTkLabel(app, image=img, text='')
panel.place(relx=0.5, rely=0.16, anchor=tkinter.CENTER)


def openfilename():
    """Processing, sending and receiving data"""
    global data_id
    global button
    button.configure(state="disabled") #Disable submit button

    # open file dialog box to select image
    # The dialogue box has a title "Open"

    try:
        client = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), keyfile='server.key', certfile='server.crt') #Initialize the SSL protocol
        client.connect((ip_server, 9090))
        filename = filedialog.askopenfilename(title='photo') #Opening File Explorer
        file = Image.open(filename)
        #Reducing the photo to 1200 pixels (without distorting the image)
        file.thumbnail(size=(1200,1200))
        buf = BytesIO()
        file.save(buf, format='JPEG')
        file = buf.getvalue()
        new_file = BytesIO(file)
        #Sending an image
        data = new_file.read(1024)
        while data:
            client.send(data)
            data = new_file.read(1024)
            if not data:
                client.send('end'.encode())
        
        #Getting data
        message = client.recv(1024)
        data_id = message.decode('utf-8')
    except:
        error()
    text_centor.set(data_id)
    client.close()
    button.configure(state="normal") #Enable submit button

def downloadThread():
    """Initializable multithreading"""
    t1 = threading.Thread(target=openfilename)
    t1.start() 


def error():
    """Action on error"""
    status_server.set('Server disconnect 🟥')
    data_id = ''
    text_centor.set('')
    if trigger_value == 1:
        lbl3 = customtkinter.CTkLabel(
            app, textvariable=status_server, font=("Arial Bold", 20))
        lbl3.place(relx=0.09, rely=0.96, anchor=tkinter.CENTER)
        lbl5 = customtkinter.CTkLabel(
            app, text='Version 1.4', font=("Arial Bold", 20))
        lbl5.place(relx=0.99, rely=0.96, anchor=tkinter.SE)
    button2 = customtkinter.CTkButton(master=app, text="Restart", command=res, font=("Arial Bold", 25))
    button2.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    button1 = customtkinter.CTkButton(master=app, text="Exit", command=ex, font=("Arial Bold", 25))
    button1.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    app.mainloop()


def res():
    """Restarting the program"""
    os.execv(sys.executable, ['python'] + sys.argv)


def ex():
    """Close the program"""
    sys.exit()


try:
    client = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), keyfile='server.key', certfile='server.crt') #Initialize the SSL protocol
    client.connect((ip_server, 9090))
    client.close()

    lbl1 = customtkinter.CTkLabel(
        app, textvariable=status_server, font=("Arial Bold", 20))
    lbl1.place(relx=0.08, rely=0.96, anchor=tkinter.CENTER)
    lbl5 = customtkinter.CTkLabel(
        app, text='Version 1.4', font=("Arial Bold", 20))
    lbl5.place(relx=0.95, rely=0.96, anchor=tkinter.CENTER)

    lbl2 = customtkinter.CTkLabel(
        app, text='Id:', textvariable=text_centor, font=("Arial Bold", 20))
    lbl2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # Use CTkButton instead of tkinter Button
    button = customtkinter.CTkButton(
        master=app, text="Upload", command=downloadThread, font=("Arial Bold", 25))
    button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

except:
    trigger_value = 1
    error()

app.mainloop()
