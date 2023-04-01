
class Event:
    def __init__(
            self, 
            id, 
            rsvp = None,
            attendees = None,
            ):
        
        self.id = id
        self.rsvp = rsvp
        self.attendees = attendees
