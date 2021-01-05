try:
    from machine import Timer
    
except:
    pass

import Servers
from Templates import MetroTiles
from Apps import Thermostat
import time

'''
#! First Launch Radenium:

from Radenium import Radenium
Radenium=Radenium.Radenium()

#! Then Create your apps:

from Radenium.Apps import Provisioning
prov_app=Provisioning.Provisioning()

#! Now hook them up with Radenium:
#! Do you want to tell all apps about the events you create in your apps?
#! Then register the addEvent function of Radenium and shoot them in as a dict. 
#! Those who understand your events will know how to deal with your events.

prov_app.Register_EventManager( Radenium.addEvent )

#! Do you require a handler to periodically call your app as if it were a main loop?

Radenium.addAppHandler(prov_app.RunHandler)

#! Do you want a UI available to a user via a web interface?

Radenium.addAppUI( prov_app.getAppDataStruct() )

#! Then you require to setup the UI server as well:
Radenium.SetUpUIServer()

#! at this point you can choose what to do:

Radenium.RunNonStop() #! makes the ui server available continue
#! You can get it out of continuous mode by calling: Radenium.RunNonStop(False)

#! To only run it one main loop (convenient for debugging) call:
Radenium.Run() #! To run once the server, make sure to call the server first by the webbrowser, other wise it will miss its call.

'''

'''
r.addAppUI( thermostatapp.getAppStruct(), thermostatapp.userInteractionCB )
r.addAppUI( provisionapp.getAppStruct(), provisionapp.userInteractionCB )
r.RunContinuous(True)
r.Run()

from Radenium import UISocket
'''

'''
So radenium launches but does not yet have the sockets launched and does not run forever yet
then anybody can add an application:

A function to shoot events to all apps
myapp.shootevent = radenium.shootevent
A function to register a handler:
radenium.handlerReg( myapp.handler )
A function to register a web ui:
radenium.AddApp( myapp.configuration )

or all is in the configuration.
So provisioning for example give information about network change or ifconfig

Dus je kan ook een console app maken die dan de events print naar het beeldscherm!

'''


class Radenium:
    def __init__( self ):
        self._RunNonStop= False
        self._ien = False
        self._Apps = [] #! Contains a list with apps name, id, userinteraction call back to be registered when the server goes online
        self._AppHandlers = []
        self._Events = []
        try:
            self.interrupt = Timer(3)
            self.interrupt.init(mode=Timer.ONE_SHOT)
            self.interrupt_ch = self.interrupt.channel(Timer.A, freq=5)  # start the event counter with a frequency of 10Hz and triggered by positive edges
        except:
            pass
            
        self._template = MetroTiles.MetroTiles()
        self._appserver = None
        
        
    def addApp( self, app ):
        try:
            app.Register_EventManager( self.addEvent )
        except:
            pass
            print("Could not register eventmanager")
            
        try:
            self.addAppHandler(app.RunHandler)
        except:
            pass
            print("Could not register run handler")
            
        try:
            print(app.getAppDataStruct())
            self.addAppUI( app.getAppDataStruct() )
        except:
            pass
            print("Could not register app UI")
        
        
    def SetUpUIServer( self ):
        self._acceptWebConnections = False
        try:
            time.sleep_ms(900)
        
        except:
            pass
            
        if self._appserver:
            self._appserver.shutdown()
            del(self._appserver)
        
        #launch the UI socket however, do not ignite the socket allready
        self._appserver = Servers.HttpServer(blocking=False)
        #Configuring the server:
        self._appserver.setTemplate( self._template )
        for apps in self._Apps:
            #! \todo should simplify the registration at the server, instead of two parameters, one is enough.
            self._appserver.addApp( apps, apps["UICB"] )
        
        try:
            time.sleep_ms(900)
        except:
            pass
        self._acceptWebConnections = True
        
    def addEvent( self, event ):
        print("\n\n!!!!!!Yo I have an Event: ", event,"\n\n")
        self._Events.append( dict( event ) )
        if event["id"] == 'provisioning':
            #! When provisioning messed around, always reconfigure the server...
            self.SetUpUIServer()
            print("Reconfiguring UI Server...")
                
        
        
        
    def addAppUI( self, dataStruct ):
        '''Currently simply reroutes to the appserver in which the routing resides to fill out the template. '''
        #I have to store the Callback function and the "com" of the appstruct I think... for if I need
        #to relaunch the AppUIServer on a change of network.
        try:
            app_exists = False
            for apps in self._Apps:
                if apps["id"] == dataStruct["id"]:
                    app_exists = True
                    
            if not app_exists:
                self._Apps.append(dict(dataStruct))
                #! \todo should simplify the registration at the server, instead of two parameters, one is enough.
                self._appserver.addApp(dataStruct, dataStruct["UICB"] )
            
        except:
            pass
        
    def addAppHandler( self, appHandler ):
        print("Adding a handler which is not yet called")
        self._AppHandlers.append( appHandler )
        
        
    def RunNonStop( self, cont=True ):
        self._RunNonStop = True
        while True:
            self.Run()
            if not self._RunNonStop:
                break;  #! Only perform the loop once if not continuous running.
        
    def Stop( self ):
        self._RunNonStop = False
        
        
    def IntEnable(self, ien=True):
        ''''\attention interrupts can be enabled before the class is initialized!'''
        if ien:
            self.interrupt_ch.irq( handler=self._RunInt, trigger=Timer.TIMEOUT)
            
        self._ien = ien
        if self._ien:
            self.ClearInt() #! Generate the first interrupt here, this might cause timing issues even though I think this is the best solution.
        
        
        
    def ClearInt(self):
        if self._ien:
            self.interrupt_ch.freq(5) #! Retrigger for a brand new and fresh interrupt...
        
        
    def _RunInt( self, int=0):
        #! \bug this does not work when interrupt is enabled, at least not Timer 3 in one shot mode interrupt...
        print( "in interrupt", int )
        print("do all stuff and reint")
        
        self.ClearInt() #! prepares for a new interrupt, this way the progam does not eat its own tail.
        
            
            
    def Run( self ):
        #if self._appserver != None:
        if self._acceptWebConnections:
            self._appserver.AcceptConnections()
            
        #pop the first event from the event list
        #run appstate = runAppHandler( popped event )
        #trace the appstates, if all are idle than we can go to sleep or so...
        try:
            for app in self._AppHandlers:
                #pop event or so. pop event[0] dus...
                app({"event":"Ja TOOOOCH"})
            
        except:
            pass
            #print("was not able to run the callback")
            
