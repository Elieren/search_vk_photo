from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser
from kivy.uix.label import Label
import socket

server = ''

kv = """
MDFloatLayout:
    FitImage:
        source: 'background.png'
    MDRaisedButton:
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
        text: "version 1.0"
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
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server, 9090))
            root.ids.server_stat.text = 'Server connect'
        except:
            root.ids.server_stat.text = 'Server disconnect'
        
        self.theme_cls.primary_palette = "Green"
        return root

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)
    
    def selected(self, selection):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server, 9090))
            file = open(f'{selection[0]}', mode='rb')
            data = file.read(1024)
            while data:
                client.send(data)
                data = file.read(1024)
                if not data:
                    client.send('end'.encode())
            file.close()

            message = client.recv(1024)
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

if __name__ == '__main__':
    FileChooser().run()