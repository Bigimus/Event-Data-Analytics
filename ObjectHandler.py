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
            root_username = data["root_username"], 
            root_password = data["root_password"]#fernet.decryptData(data["root_password"])  # noqa: E501
        ) -> None:
        #self.fernet = Security(Configurations.FERNET)
        self.root_username:str = root_username
        self.root_password:str = root_password
    
    def saveSettings(self):
        data = SH.readJson(Configurations.SETTINGS)
        data["root_username"] = self.root_username
        data["root_password"] = self.root_password#self.fernet.encryptData(self.root_password)  # noqa: E501
        SH.writeJson(Configurations.SETTINGS, data)

