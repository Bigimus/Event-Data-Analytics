from dataclasses import dataclass

# from cryptography.fernet import Fernet

import StorageHandler as SH

@dataclass
class Configurations:
    ## FILES $$
    SETTINGS:str = "Configs/Settings.json"
    UI:str = "Configs/UI.kv"

class Settings:
    data = SH.readJson(Configurations.SETTINGS)
    #fernet = Security(Configurations.FERNET)
    def __init__(
            self, 
            username = data["root"]["username"], 
            password = data["root"]["password"]#fernet.decryptData(data["root_password"])  # noqa: E501
        ) -> None:
        #self.fernet = Security(Configurations.FERNET)
        self.username:str = username
        self.password:str = password
    
    def saveSettings(self):
        data = SH.readJson(Configurations.SETTINGS)
        data["root"]["username"] = self.username
        data["root"]["password"] = self.password#self.fernet.encryptData(self.root_password)  # noqa: E501
        SH.writeJson(Configurations.SETTINGS, data)

class Event:
    def __init__(self, id, name = None, location = None, date = None):  # noqa: E501
        self.id = id
        self.name = name
        self.location = location
        self.date = date
    
    def createEvent(self):
        command = """
            INSERT INTO event_info (
                id, 
                name,
                location, 
                date
            ) VALUES (%s, %s, %s, %s); """
        values = (
            self.id,
            self.name,
            self.location,
            self.date
        )
        print(command, values)
    
    def deleteEvent(self):
        command = "DELETE FROM event_info WHERE id = %s"
        value = self.id
        print(command, value)


