from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser
from kivy.uix.label import Label
import threading
from kivy.clock import mainthread, Clock
import cv2
import io
import requests
import json

ip_server = '' #Flask server

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
            response = requests.post(f'{ip_server}/')
            root.ids.server_stat.text = 'Server connect'
        except:
            root.ids.server_stat.text = 'Server disconnect'

        
        self.theme_cls.primary_palette = "Green"
        return root

    def file_chooser(self):
        filechooser.open_file(on_selection=self.downloadThread)
    
    def selected(self, selection):
        self.button_off()
        self.root.ids.selected_path.text = ''
        try:
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
            files = {'image': ('1.jpg', new_file, f'image/jpeg')}
            response = requests.post(f'{ip_server}/api', files=files)
            
            d = []
            a = response.json()
            for i in a:
                status = json.loads(i)['status']
                if status == '🟢':
                    id_a = json.loads(i)['id']
                    name = json.loads(i)['name']
                    bdate = json.loads(i)['bdate']
                    city = json.loads(i)['city']
                    country = json.loads(i)['country']
                    d.append(f'• id: {id_a}, name: {name}, bdate: {bdate}, city: {city}, country: {country}')
                else:
                    text = json.loads(i)['text']
                    d.append(f'--- {text}')
            data_id = '\n'.join(d)
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