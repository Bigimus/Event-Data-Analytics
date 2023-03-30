import mysql.connector as sql

from SettingsHandler import Settings

import StorageHandler as SH

class Database:
    settings = SH.readJson(Settings.SETTINGS)["database"]
    def __init__(
            self, 
            host = settings["host"], 
            username = settings["username"], 
            password = settings["password"], 
            database = settings["database"]
            ):
        
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

    def sendCommand(self, command, values):
        self.cursor.executemany(command, (values, ))