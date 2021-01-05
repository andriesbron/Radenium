from Core.App import App

class Settings(App):
    def boot(self):
        self.setTitle("Settings")
        self.setDescription("Manage SocialHome settings.")
        self.ui.addElement("button", "updatefirmware", "", "Update Firmware", "")
        self.ui.addElement("text", "city", "", "City where this Radenium instance is used.", "")
        self.ui.addElement("text", "lat", "", "Latitude of city (overrides city)", "")
        self.ui.addElement("text", "lon", "", "Longitued of city (overrides city)", "")

    def appSettings(self):
        pass
        #! @todo Somehow view app settings here?

    def renderAppModules(self, position, request):

        if position == "attribution":
            attr = ""
            for p in self.process():
                if (p.find('Service.') + p.find('App.')) >= 0:
                    if self.process()[p].attribution() != '':
                        attr += '<h4>'+self.process()[p].getTitle()+'</h4><p>'+self.process()[p].getDescription()+'</p><p>'+self.process()[p].attribution()+'</p>'
            
            return attr

    def onButtonPressed(self, button):
        if button == "updatefirmware":
            self.process()['Service.UserAlerts'].alert('System was updated.')
            