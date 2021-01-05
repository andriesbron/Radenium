
#! DO NOT MODIFY THIS FILE
from Core.Service import Service

class Widget(Service):
    '''Root widget class
    
    Extends the root process is basically to create visual data for a user, however, not to be controlled.
    It could give an information display to a service. Maybe, eventually, the app should extend this class. '''

    def __init__(self, procPointer):
        super().__init__(procPointer)
    
    def embedCode(self):
        return "the stuff in iframe"

    def renderWidget(self, type="html"):
        return "geen iframe, wel a tag met gif, divs of wat ook maar, als het maar van de form van type  is. embedcode stopt het in iframe, is ook html maar anders."
