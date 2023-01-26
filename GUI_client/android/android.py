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
        size_hint: .5, .5
    MDLabel:
        id: version
        text: "version 1.0"
        pos_hint: {"right": 1.8 , "center_y": .06 }
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_size: 14
    MDLabel:
        id: server_stat
        text: ""
        pos_hint: {"right": 1.02 , "center_y": .06 }
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_size: 14
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
            self.root.ids.server_stat.text = 'Server connect'
        except:
            data_id = ''
            self.root.ids.server_stat.text = 'Server disconnect'
        self.root.ids.selected_path.text = (data_id)

if __name__ == '__main__':
    FileChooser().run()