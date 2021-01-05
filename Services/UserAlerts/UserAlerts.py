
from Core.Service import Service

class UserAlerts(Service):
    def __init__(self,procPointer):
        super().__init__(procPointer)
        self.setTitle("Debug Service")
        # @todo open a file to write to.
        self.alerts={'error':[], 'warning':[], 'success':[],'info':[]}
        

    def alert(self, alert, type="info"):
        if type in self.alerts:
            self.alerts[type].append(alert)
        
    def render(self):
        alerts=""
        if len(self.alerts['error']) > 0:
            alerts+="<div class=\"alert alert-danger\"><h4>Error</h4>"
            for al in self.alerts['error']:
                alerts += "<p>" + al + "</p>\n"
            alerts += "</div>"

        if len(self.alerts['warning']) > 0:
            alerts+="<div class=\"alert alert-warning\"><h4>Warning</h4>"
            for al in self.alerts['warning']:
                alerts += "<p>" + al + "</p>\n"
            alerts += "</div>"

        if len(self.alerts['info']) > 0:
            alerts+="<div class=\"alert alert-info\"><h4>Information</h4>"
            for al in self.alerts['info']:
                alerts += "<p>" + al + "</p>\n"
            alerts += "</div>"

        if len(self.alerts['success']) > 0:
            alerts+="<div class=\"alert alert-success\"><h4>Success</h4>"
            for al in self.alerts['success']:
                alerts += "<p>" + al + "</p>\n"
            alerts += "</div>"

        #! Once rendered all information is cleared.
        self.alerts={'error':[], 'warning':[], 'success':[],'info':[]}

        return alerts




