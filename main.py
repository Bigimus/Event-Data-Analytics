from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen 
from kivymd.uix.menu import MDDropdownMenu

from ObjectHandler import Configurations as Config
from ObjectHandler import Settings
from ObjectHandler import Event
from DatabaseHandler import Database

import StorageHandler as SH

UI = Config.UI
SETTINGS = Config.SETTINGS

Window.size = 1280, 720

class LoginWindow(MDScreen):
    def validateLogin(self, username, password):
        if username == Settings().root_username and password == Settings().root_password:   # noqa: E501
            return "True"
        else: 
            return "False"

class HomeWindow(MDScreen):
    pass

class SettingsWindow(MDScreen):
    def saveRoot(self, username, password):
        self.settings = Settings(
            username, 
            password
        ).saveSettings()

    def saveDatabase(self, host, username, password, database):
        self.database = Database(
            host,
            username,
            password,
            database
        ).saveSettings()

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
        ).createEvent()

        self.ids.client_id.text = ""
        self.ids.event_name.text = ""
        self.ids.event_location.text = ""
        self.ids.event_date.text = ""

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