

######### DO NOT EDIT BELOW THIS
try:
    import tracemalloc
except:
    pass

import time
from Core.htmltpl import htmltpl
from Modules.Platform import Platform

#Service imports
#! from directory.directory import file
from Services.Debugging import Debugging
from Services.Storage import Storage
from Services.UserAlerts import UserAlerts
from Services.Scheduler import Scheduler
from Services.Ntp import Ntp
#from Services.Sdp import Sdp

#App imports


from Apps.Automator import Automator
from Apps.SystemConfiguration import Settings
from Apps.Provisioning import Provisioning

#! @todo create a baseSH for  apps and services that contains the tick story etcetera, not to maintain duplicate code.
class Radenium:
    _processDict = {}
    def __init__(self, runLoopSleep=0):
        '''Initializes Radenium

        In case you can accept a rundelay, for example, to reduce the python load on your mac Pro, you can set a sleep time at run.'''

        try:
            tracemalloc.start()
        except:
            pass

        self._runLoopSleep = runLoopSleep
        self._sh_pace = 1
        self._homeWidget="""<h1>Set A Homepage</h1><p>You can set your own HTML on the home page using Radenium.setHomeWidget('''...here goes your html...''')</p>"""
        self._apps =[]
        self._services = []
        self._serviceDict = {}
        self._processes = []


        Radenium._processDict['Radenium'] = Platform.Platform()

        #! first setup services
        self._processes.append(Debugging.Debug(self.process))
        self._processes.append(Storage.Storage(self.process))
        self._processes.append(UserAlerts.UserAlerts(self.process))
        self._processes.append(Ntp.Ntp(self.process))
        #self._processes.append(Scheduler.Scheduler(self.process))
        

        #! Loading of the apps influences menu order.
        self._processes.append(Automator.Automator(self.process))
        self._processes.append(Settings.Settings(self.process))
        self._processes.append(Provisioning.Provisioning(self.process))

        for s in self._processes:
            Radenium._processDict[s.iam()]=s

        #! Running the boot levels
        for p in self._processes:
            p.bootService(0)
        for p in self._processes:
            p.bootService(1)
        #! And boot
        for p in self._processes:
            if 'App' in p.iam():
                p.boot()

        self._isRunning=True
        self.log(self.process()['Radenium'].system())
        self.log("Radenium instantiated, have fun!")
        self.process()['Service.UserAlerts'].alert("Great you are back!","success")

        try:
            current, peak = tracemalloc.get_traced_memory()
            self.log("Mem usage: %sMB; Peak was %sMB"%(current / 10**6, peak / 10**6))
            tracemalloc.stop()
        except:
            pass

    def log(self, msg, type="INFO"):
        try:
            Radenium._processDict['Service.Debug'].log(msg, type)
        except:
            pass

    def addProcess(self, process):
        self.log("Adding process "+process.iam())
        self._processes.append(process)
        Radenium._processDict[process.iam()]=process
        #! Running the boot levels
        process.bootService(0)
        process.bootService(1)
        #! And boot if it's an app
        if 'App' in process.iam():
            self.log("This process is an app, booting app " + process.iam())
            process.boot()

    def killProcess(self, processName):
        found = False
        self.log("Attacking " + processName)
        for i, p in enumerate (self._processes):
            if p.iam() == processName:
                #! Delete first from dict
                del (Radenium._processDict[processName])
                del(self._processes[i])
                found=True

        if found:
            self.log(processName+" died.")
        else:
            self.log("He won, could not find "+processName+".")

    def process(self):
        return Radenium._processDict

    def system(self):
        return {"platform":_PLATFORM_}

    def getAppName(self,id):
        return self._apps[id].__class__.__name__

    @staticmethod
    def parseUrlQuery(query):
        urlpars = {}
        try:
            for q in query.split('&'):
                qsplit=q.split('=')
                urlpars[qsplit[0]] = qsplit[1]
        except:
            pass

        return urlpars
    def setHomeWidget(self,component):
        self._homeWidget=component

    def homeWidget(self):
        return self._homeWidget

    def httpRequest(self, query, request):
        q = self.parseUrlQuery(query)
        tpl = htmltpl()
        for proc in self._processes:
            #! Add menu items to the template, if the application has a menu link (services and processes don't).
            try:
                tpl.addMenu(proc.menuLink())
            except:
                pass

        if not 'App' in q:
            tpl.setComponent(self.homeWidget())

        else:
            for proc in self._processes:
                if proc.__class__.__name__ == q['App']:
                    tpl.setComponent(proc.getHttpRequest(q, request)['response'])
                    tpl.setTitle(proc.getTitle())
                    tpl.setDescription(proc.getDescription())

        tpl.setNotifications(self.process()['Service.UserAlerts'].render())

        return tpl.render()

    def run(self):
        try :
            while self._isRunning:
                self.runOnce()
                #! A little sleep on a mac system..

        except KeyboardInterrupt :
            pass

    def runOnce(self):
        start = time.time()
        elapsed = 0
        try:
            tracemalloc.start()
        except:
            pass

        #! Check runLoopSleep prior to entering the fast loop, other wise the fast loop continuously checks, I don't like that.
        while elapsed < self._sh_pace:
            elapsed = time.time() - start
            for p in self._processes:
                p.run()

            time.sleep(self._runLoopSleep)

        for p in self._processes:
            p.tickHandler(self._sh_pace)

        try:
            current, peak = tracemalloc.get_traced_memory()
            if peak > 10000:
                self.log("Mem usage: %sMB; Peak was %sMB"%(current / 10**6, peak / 10**6))
            tracemalloc.stop()

        except:
            pass

    def halt(self):
        self.log("")
        self.log("")
        self.log("")
        self.log("If we don't slow this fire down, we're not gonna last")
        self.log("Cool the engines")
        self.log("Red line's gettin' near")
        self.log("Cool the engines")
        self.log("Better take it out of gear")
        self.log("We don't have to run that hard to get where we can go")
        for proc in self._processes:
            proc.halt()

        self.log("")
        self.log("...Engines cooled down.")
