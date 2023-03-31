from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen 
from kivymd.uix.menu import MDDropdownMenu

from SettingsHandler import Settings
from EventHandler import Event

import StorageHandler as SH

UI = Settings.UI
SETTINGS = Settings.SETTINGS

Window.size = 1280, 720

class LoginWindow(MDScreen):
    def validateLogin(self, username, password):
        if username == Settings().root_user and password == Settings().root_pass:   # noqa: E501
            return "True"
        else: 
            return "False"

class HomeWindow(MDScreen):
    pass

class SettingsWindow(MDScreen):
    def saveSettings(self, root_user, root_pass, host, db_user, db_pass, database):
        Settings(
            root_user = root_user, 
            root_pass = root_pass,
            host = host,
            db_user = db_user,
            db_pass = db_pass,
            database = database
        ).save()

    ## CLIENTS ##

    def openClientMenu(self):
        data = SH.readJson(SETTINGS)
        clients = [
            {
            "text": f"{client}",
            "viewclass": "OneLineListItem",
            "on_release": lambda x = f"{client}": self.setClient(x)
            } for client in data["client_ids"]
        ]
        self.client_menu = MDDropdownMenu(
            caller = self.ids.client_id,
            items = clients,
            width_mult = 3,
            position = "bottom",
            max_height = dp(224)
        )
        self.client_menu.open()
    
    def setClient(self, client):
        self.ids.client_id.text = f"{client}"
        self.client_menu.dismiss()
    
    def deleteClientID(self, client_id):
        data = SH.readJson(SETTINGS)
        data["client_ids"].remove(client_id)
        SH.writeJson(SETTINGS, data) 
        self.ids.client_id.text = ""

    def createClientID(self, client_id):
        data = SH.readJson(SETTINGS)
        data["client_ids"].append(client_id)
        SH.writeJson(SETTINGS, data)
        self.ids.client_id.text = ""
    
class CreateWindow(MDScreen):
    def openClientMenu(self):
        data = SH.readJson(SETTINGS)
        clients = [
            {
            "text": f"{client}",
            "viewclass": "OneLineListItem",
            "on_release": lambda x = f"{client}": self.setClient(x)
            } for client in data["client_ids"]
        ]
        self.client_menu = MDDropdownMenu(
            caller = self.ids.client_id,
            items = clients,
            width_mult = 4,
            position = "bottom",
            max_height = dp(224)
        )
        self.client_menu.open()
    
    def setClient(self, client):
        self.ids.client_id.text = f"{client}_1"
        self.client_menu.dismiss()
    
    def createAccount(self, client_id:str, event_name, event_location, event_date):
        client_id = client_id.split("_")
        event_id = client_id[1]
        client_id = client_id[0]

        Event(
            client_id,
            event_id,
            event_name,
            event_location,
            event_date
        ).create()

        self.ids.client_id.text = ""
        self.ids.event_name.text = ""
        self.ids.event_location.text = ""
        self.ids.event_date.text = ""

class EventWindow(MDScreen):
    def validateEventNum(self, event_num):
        try:
            event_num = int(event_num)
            return True
        except ValueError:
            return False
    
    def clear(self):
        self.ids.event_num.text = ""
        self.ids.name.text = ""
        self.ids.location.text = ""
        self.ids.date.text = ""

    def openClientMenu(self):
        data = SH.readJson(SETTINGS)
        clients = [
            {
            "text": f"{client}",
            "viewclass": "OneLineListItem",
            "on_release": lambda x = f"{client}": self.setClient(x)
            } for client in data["client_ids"]
        ]
        self.client_menu = MDDropdownMenu(
            caller = self.ids.client_id,
            items = clients,
            width_mult = 4,
            position = "bottom",
            max_height = dp(224)
        )
        self.client_menu.open()
    
    def setClient(self, client):
        self.ids.client_id.text = f"{client}"
        self.client_menu.dismiss()
    
    # 1a
    def search(self):
        client_id = self.ids.client_id.text
        event_num = self.ids.event_num.text
        event_id = client_id + "_" + event_num
        self.event = Event(event_id)
        self.event.search()
        self.ids.name.text = self.event.name
        self.ids.location.text = self.event.location
        self.ids.date.text = self.event.date
        self.ids.edit.disabled = False
    
    # 1b
    def create(self):
        self.event = Event(
            id = f"{self.ids.client_id.text}_{self.ids.event_num.text}",
            name = self.ids.name.text,
            location = self.ids.location,
            date = self.ids.date.text
        )
        self.event.create()
        self.clear()

    # 2
    def edit(self):
        self.ids.save.disabled = False
        self.ids.delete.disabled = False

    # 3
    def save(self):
        self.event.name = self.ids.name.text
        self.event.location = self.ids.location.text
        self.event.date = self.ids.date.text
        self.event.save()
        
class WindowManager(MDScreenManager):
    pass

class MainApp(MDApp):
    data = SH.readJson(SETTINGS)
    client_ids = ",\n".join(data["client_ids"])
    root_username = data["root"]["username"]
    root_password = data["root"]["password"]

    ## DATABASE ##
    host = data["database"]["host"]
    database_username = data["database"]["username"]
    database_password = data["database"]["password"]
    database = data["database"]["database"]

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.title = "Event Data Analytics"
        self.kv = Builder.load_file(UI)
        self.loadSettings()
        return self.kv
    
    def validateData(*args):
        for arg in args:
            if arg == "" and args.index(arg) != 0:
                return False
            else:
                pass
        return True
    
    def loadSettings(self):
        data = SH.readJson(SETTINGS)   

        ## ROOT ##

        self.root_username = data["root"]["username"]
        self.root_password = data["root"]["password"]

        ## DATABASE ##

        self.host = data["database"]["host"]
        self.database_username = data["database"]["username"]
        self.database_password = data["database"]["password"]
        self.database = data["database"]["database"]

        ## CLIENT ##

        self.client_ids = ",\n".join(data["client_ids"])

MainApp().run()