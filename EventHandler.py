
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


