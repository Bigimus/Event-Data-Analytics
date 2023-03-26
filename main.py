from kivy.core.window import Window
from kivy.lang import Builder
# from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen 
# from kivymd.uix.menu import MDDropdownMenu

from ObjectHandler import Configurations as Config
from ObjectHandler import Settings


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

class WindowManager(MDScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.title = "Event Data Analytics"
        self.kv = Builder.load_file(UI)
        return self.kv
    
    def validateData(*args):
        for arg in args:
            if arg == "" and args.index(arg) != 0:
                return False
            else:
                pass
        return True
    
MainApp().run()