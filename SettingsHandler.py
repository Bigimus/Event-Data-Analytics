import StorageHandler as SH

class Settings:
    SETTINGS = "Configs/Settings.json"
    UI = "Configs/UI.kv"
    data = SH.readJson(SETTINGS)
    def __init__(
            self, 
            root_user = data["root"]["username"], 
            root_pass = data["root"]["password"],
            client_ids = data["client_ids"],
            host = data["database"]["host"],
            db_user = data["database"]["username"],
            db_pass = data["database"]["password"],
            database = data["database"]["database"]
        ) -> None:
        self.root_user:str = root_user
        self.root_pass:str = root_pass
        self.client_ids:list = client_ids
        self.host:str = host
        self.db_user:str = db_user
        self.db_pass:str = db_pass
        self.database:str = database
    
    def save(self):
        print("save")
        data = SH.readJson(self.SETTINGS)
        data["root"]["username"] = self.root_user
        data["root"]["password"] = self.root_pass
        data["client_ids"] = self.client_ids
        data["database"]["host"] = self.host
        data["database"]["username"] = self.db_user
        data["database"]["password"] = self.db_pass
        data["database"]["database"] = self.database
        print(data)
        SH.writeJson("Configs/Settings.json", data)