import mysql.connector as sql

from ObjectHandler import Configurations as Config

import StorageHandler as SH

class Database:
    settings = SH.readJson(Config.SETTINGS)["database"]
    def __init__(self, host = settings["host"], username = settings["username"], password = settings["password"], database = settings["database"]):  # noqa: E501
        self.host = host
        self.username = username
        self.password = password
        self.database = database

        self.connection = sql.connect(
            host = self.host,
            user = self.username,
            password = self.password,
            database = self.database
        )
        self.cursor = self.connection.cursor()
    
    def saveSettings(self):
        data = SH.readJson(Config.SETTINGS)
        data["database"]["host"] = self.host
        data["database"]["username"] = self.username
        data["database"]["password"] = self.password
        data["database"]["database"] = self.database
        SH.writeJson(Config.SETTINGS, data)

    def sendCommand(self, command, values):
        self.cursor.executemany(command, (values, ))