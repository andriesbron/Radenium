
from Core.App import App

try:
    import pycom
    import machine
    from network import WLAN
    _PLATFORM_="ESP32"

except:
    _PLATFORM_="PC"

class Provisioning(App):
    def boot(self):
        self.setTitle("Provisioning")
        self.setDescription("Provision with a network at your location.")
        self.ui.addElement("select", "network", 2, "Select A Network", "",options={"options":self.scanForNetworks()})
        self.ui.addElement("text", "othernetwork", "", "Other Network SSID", "",placeholder="Provide a network not in the list.")
        self.ui.addElement("select", "security", 2, "Network Security", "",options={"options":{"0": "No Security","1":"WPA","2":"WPA2"}})
        self.ui.addElement("password", "pass", "", "Network Pass Phrase", "")
        self.ui.addElement("button", "provision", "provision", "Provision!", "")

        try:
            self.wlan = WLAN()

        except:
            pass #! This platform is not the WiPy.

    def scanForNetworks(self):
        nlist={}
        if _PLATFORM_=="ESP32":
            wlan = WLAN(mode=WLAN.STA)
            networks =  wlan.scan()
            wlan.mode(WLAN.AP)
            
            for n in networks:
                nlist[n[0]]= n[0]+", rssi "+str(n[4])

        elif _PLATFORM_=="PC":
            pass
            nlist['null'] = 'No networks found.'

        return nlist

    def onButtonPressed(self, button):
        if button=='provision':
            self.log("Provisioning")
            self.log(self.ui.elements['network'].value)
            self.log(self.ui.elements['othernetwork'].value)
            self.log(self.ui.elements['security'].value)
            self.log(self.ui.elements['pass'].value)



    def provision(self, ssid, password, security):
        try:
            wlan=WLAN()
            wlan.mode(WLAN.STA)
            authtype = int(security)
            wlan.connect(ssid, auth=( authtype, password), timeout=5000)
            while not wlan.isconnected():
                self._callBack({'Provisioning':True, 'ip':self.wlan.ifconfig()})
                self.log("Provisioning successful, ip address: "+str(self.wlan.ifconfig()))
        
        except:
            self.log("Provisioning failed.")
            wlan.mode(WLAN.AP)
            self._callBack({'Provisioning':True, 'ip':self.wlan.ifconfig()})
