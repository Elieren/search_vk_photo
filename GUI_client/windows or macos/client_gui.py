import tkinter
import customtkinter
from tkinter import filedialog
from tkinter import StringVar
import os
import sys
from PIL import ImageTk, Image
from io import BytesIO
import threading
import requests
import json

ip_server = '' #Flask server

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
    global data_id
    global button
    button.configure(state="disabled")

    # open file dialog box to select image
    # The dialogue box has a title "Open"

    try:
        d = []
        filename = filedialog.askopenfilename(title='photo')
        file = Image.open(filename)
        file.thumbnail(size=(1200,1200))
        buf = BytesIO()
        file.save(buf, format='JPEG')
        file = buf.getvalue()
        new_file = BytesIO(file)
        files = {'image': ('1.jpg', new_file, f'image/jpeg')}
        response = requests.post(f'{ip_server}/api', files=files, verify=False, cert=('server.crt','server.key'))

        a = response.json()
        for i in a:
            status = json.loads(i)['status']
            if status == '🟢':
                id_a = json.loads(i)['id']
                name = json.loads(i)['name']
                bdate = json.loads(i)['bdate']
                city = json.loads(i)['city']
                country = json.loads(i)['country']
                d.append(f'🟢 id: {id_a}, name: {name}, bdate: {bdate}, city: {city}, country: {country}')
            else:
                status = json.loads(i)['status']
                text = json.loads(i)['text']
                d.append(f'{status} {text}')
        data_id = '\n'.join(d)

        print(data_id)
    except:
        error()
    text_centor.set(data_id)
    button.configure(state="normal")

def downloadThread():
    t1 = threading.Thread(target=openfilename)
    t1.start() 


def error():
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
    os.execv(sys.executable, ['python'] + sys.argv)


def ex():
    sys.exit()


try:
    response = requests.get(f'{ip_server}/', verify=False, cert=('server.crt','server.key'))

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
