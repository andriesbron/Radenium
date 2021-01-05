
from Core.App import App


class Thermostat(App):  
    def onValueChanged(self, element, oldVal, newVal):
        print(element)

    def onButtonPressed(self, button):
        if button == "tempup":
            #self.ui.elements['settemp'].value = float(self.ui.elements['settemp'].value) + 0.5
            self.ui.setVal("settemp", float(self.ui.elements['settemp'].value) + 0.5)

        elif button == "tempdown":
            #self.ui.elements['settemp'].value = float(self.ui.elements['settemp'].value) - 0.5
            self.ui.setVal("settemp", float(self.ui.elements['settemp'].value) - 0.5)

    def serviceCB(self, event, dataFunc=None):
        if event == 'Service.Scheduler.sunset.now':
            #! Increase the set temperatuur with a 0.3 degrees.
            pass
        elif event == 'Service.Scheduler.sunrise.now':
            #! Decrease the set temperatuur with a 0.3 degrees.
            pass
        
        #print(event)


    def boot(self):
        self.setTitle("Thermostat")
        self.setDescription("Super Python Thermostat.")
        try:
            self.process()['Service.Scheduler'].register(self.serviceCB)
        except:
            pass
        #self.ui.addInput("select", "securitytype", 2, "Network Security", "",options={"options":{"0": "No Security","1":"WPA","2":"WPA2"}})
        self.ui.addElement("button", "tempup", "tempup", "Increase Temperature", "")
        self.ui.addElement("button", "tempdown", "tempdown", "Lower Temperature", "")
        self.ui.addElement("text", "icalurl", "", "Remote Ical Thermostat Program", "", placeholder="Provide an ical url with codes to control this app.")
        self.ui.addElement("indicator", "settemp", "20.5", "Set Temperature", "")
        self.ui.addElement("indicator", "roomtemp", "20.5", "Room Temperature", "")

        self._triggers.append({'def':self.ui.getElement('settemp')})

        self.ui.setMax("settemp", 24)
        self.ui.setMin("settemp", 15)
