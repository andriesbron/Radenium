
#! Importing and launching radenium with a sleep of 0.2 seconds in the fast loop.
#! On an embedded system like ESP, you might want to put there zero.
from Core.Radenium import Radenium
sh = Radenium(runLoopSleep=0.2)


#! Create a home widget on the home page by setting the html for it.
#! This example includes a widget that does not work when in AP mode, that's obvious.
#sh.homeWidget("""<h1>Home page</h1><h2>Weather</h2><div><a href="https://www.buienradar.nl" target="_blank"><img border="0" src="https://image.buienradar.nl/2.0/image/single/RadarMapRainNL?height=512&width=500&renderBackground=True&renderBranding=True&renderText=True"></a>""")

#! Adding the Thermostat App. Make sure that the pattern of your apps or
# services follow:
#! from Apps.[yourappname] import [yourappname]
from Apps.Thermostat import Thermostat
sh.addProcess(Thermostat.Thermostat(sh.process))

#! Adding the simple not finished yet Feedreader app that currently only works on PC's
#! and immediately kill it again, to demonstrate killing of a process.
from Apps.FeedReader import FeedReader
sh.addProcess(FeedReader.FeedReader(sh.process))

#! If you run the framework on a PC and you want to see the feed reader application,
#! comment the following line
sh.killProcess('App.FeedReader')


###############################################################################
#! NO NEED TO EDIT BELOW THESE LINES, UNLESS YOU WANT TO.
###############################################################################
from time import sleep
from _thread import allocate_lock

try:
    from MicroWebSrv2  import *

except:
    print("Radenium requires MicroWebSrv2, add it to the Radenium directory.")
    print("Exciting now.")
    exit(0)

@WebRoute(GET, '/', name='Radenium1/1')
def RequestHome(microWebSrv2, request) :
    content = sh.httpRequest(request.QueryString, request=request.GetPostedURLEncodedForm())
    request.Response.ReturnOk(content)

@WebRoute(POST, '/', name='Radenium1/2')
def RequestHome(microWebSrv2, request) :
    content = sh.httpRequest(request.QueryString, request=request.GetPostedURLEncodedForm())
    request.Response.ReturnOk(content)

mws2 = MicroWebSrv2()
mws2.SetEmbeddedConfig()
mws2.NotFoundURL = '/'
mws2.StartManaged()

sh.log("You made it till here!")
sh.log("Open a browser and point it to 0.0.0.0:8080 (hardcoded and default ip:port combination)")
sh.log("See you there!")

try :
    while mws2.IsRunning :
        sh.runOnce()

except KeyboardInterrupt :
    pass

sh.halt()
mws2.Stop()
sh.log('Bye')
