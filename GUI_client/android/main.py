from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser
from kivy.uix.label import Label
import socket
import threading
from kivy.clock import mainthread, Clock
import cv2
import io
import ssl

server = ''

kv = """
MDFloatLayout:
    FitImage:
        source: 'background.png'
    MDRaisedButton:
        id: button_up
        text: "Upload"
        pos_hint: {"center_x": .5, "center_y": .3}
        on_release:
            app.file_chooser()
    MDLabel:
        id: selected_path
        text: "Upload a photo to get information about a person."
        halign: "center"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
    Image:
        source: 'banner.png'
        pos_hint: {"center_x": .5, "center_y": .8}
        size_hint: 1, 1
    MDLabel:
        id: version
        text: "Version 1.4"
        pos_hint: {"right": 1.88 , "center_y": .02 }
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_size: 24
    MDLabel:
        id: server_stat
        text: ""
        pos_hint: {"right": 1.02 , "center_y": .02 }
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_size: 24
"""

class FileChooser(MDApp):

    def build(self):
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.READ_EXTERNAL_STORAGE])
        root = Builder.load_string(kv)
        try:
            client = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), keyfile='server.key', certfile='server.crt', server_side=False)
            client.connect((server, 9090))
            root.ids.server_stat.text = 'Server connect'
        except:
            root.ids.server_stat.text = 'Server disconnect'

        
        self.theme_cls.primary_palette = "Green"
        return root

    def file_chooser(self):
        filechooser.open_file(on_selection=self.downloadThread)
    
    def selected(self, selection):
        key = self.directory + '/server.key'
        crt = self.directory + '/server.crt'
        self.button_off()
        self.root.ids.selected_path.text = ''
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            long = ssl.wrap_socket(client, keyfile=key, certfile=crt, server_side=False)
            long.connect((server, 9090))
            #----------------------------#
            image = cv2.imread(selection)
            scale_percent = 99
            k = [1200, 1200]
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)

            while True:
                if (k[0] < width) or (k[1] < height):
                    scale_percent -= 1
                    width = int(image.shape[1] * scale_percent / 100)
                    height = int(image.shape[0] * scale_percent / 100)
                else:
                    break
            
            dim =(width, height)

            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            image_bytes = cv2.imencode('.jpeg', resized)[1].tobytes()
            #----------------------------#
            new_file = io.BytesIO(image_bytes)
            data = new_file.read(1024)
            while data:
                long.send(data)
                data = new_file.read(1024)
                if not data:
                    long.send('end'.encode())

            message = long.recv(1024)
            data_id = message.decode('utf-8')
            data_id1 = data_id.split('\n')
            data_id = []
            for x in range(len(data_id1)):
                data_id2 = data_id1[x]
                data_id3 = data_id2[2:]
                if data_id3[:2] == 'id':
                    data_id3 = '• ' + data_id3
                data_id.append(data_id3)
            data_id = '\n'.join(data_id)
            self.root.ids.server_stat.text = 'Server connect'
        except:
            data_id = ''
            self.root.ids.server_stat.text = 'Server disconnect'
        self.root.ids.selected_path.text = (data_id)
        self.button_on()
    
    def downloadThread(self, selection):
        t1 = threading.Thread(target=self.selected, args = selection)
        t1.start() 
    
    @mainthread
    def button_off(self):
        self.root.ids.button_up.disabled = True
    
    @mainthread
    def button_on(self):
        self.root.ids.button_up.disabled = False

if __name__ == '__main__':
    FileChooser().run()