#from DatabaseHandler import Database

# from cryptography.fernet import Fernet

class Event:
    def __init__(
            self, 
            id, 
            name = None, 
            location = None, 
            date = None
            ):
        
        self.id = id
        self.name = name
        self.location = location
        self.date = date
    
    def create(self):
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
    
    def delete(self):
        command = "DELETE FROM event_info WHERE id = %s"
        value = self.id
        print(command, value)

    def search(self):
        command = "SELECT * FROM events WHERE name = %s"
        value = self.id
        #results = Database().sendCommand(command = command, values = value)
        print(command, value)
        self.name = "Example"
        self.location = "Example"
        self.date = "Example"
    
    def save(self):
        command = """
                    UPDATE events
                    SET 
                        name = %s,
                        location = %s,
                        date = %s
                    WHERE
                        id = %s;
                """
        values = (self.name, self.location, self.date, self.id)
        #results = Database().sendCommand(command = command, values = values)
        print(command, values)