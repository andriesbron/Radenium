
class Process:
    '''Root process class
    
    Can be extended as a service without callback functionality. 
    In case callback functionality is required, extend the Service class as a service.'''
    process = None
    def __init__(self, procPointer):
        self._sysTick = 1 # for asynchroneous enter 0
        self._sysTickCount = 0
        self._title="Root Process"
        self._description=""
        if Process.process == None:
            Process.process=procPointer

    def log(self, log, type="INFO"):
        '''Log messages

        You can throw anything in the log, casting to str happens here.'''
        try:
            Process.process()['Service.Debug'].log(self.iam()+"-"+str(log), type)
        except:
            #! Apparently, no Service.Debug instantiated.
            pass

    def setTitle(self, title):
        '''Title of process

        Set a title to recognize the process in applications, services and api interaction. 
        Used for user interaction, not between instances.'''

        self._title=title

    def setDescription(self, desc):
        '''Description of process

        Set a description to explain, in short, what the process, service or application is doing. 
        Used for user interaction, not between instances.'''

        self._description=desc

    def getTitle(self):
        return self._title

    def getDescription(self):
        return self._description

    def setTick(self, tickValue):
        ''' Process, service or application tick

        The pace on which the process is running. In steps of 1 second.
        Minimum value: 1 second.'''
        self._sysTick = tickValue > 0 and tickValue or 1

    def tickValue(self):
        return self._sysTick

    def iam(self):
        '''Process identifier

        Used as an identifier throughout the framework.'''

        return __class__.__name__ +"."+ self.__class__.__name__

    def sayHi(self, fromwho="This Process"):
        '''Say's 'Hi' to you.
        
        Can be used to check if what you build is working. I used it many times.'''

        print(str(fromwho) + " say's Hi to you!")

    def tickHandler(self, tick):
        '''Handler

        Is called by the radenium core class. Calculates for the tick call, self.tick() and call self.run(). 
        Nothing exciting from that perspective.'''
        self._sysTickCount += tick
        if self._sysTickCount >= self._sysTick:
            self._sysTickCount = 0
            self.tick()
            
    def run(self):
        '''Asynchroneous process handler.
        
        This method is to be overloaded.'''
        
        pass
    
    def tick(self):
        '''Runs on tick, pace is specified by self.setTick(), default is 1 second. 
        
        This method is to be overloaded.'''
        
        pass

    def bootService(self, level):
        '''Service boot level

        For booting services, prior to the apps. 
        Is called once all apps and services have been instantiated.
        BootService comprises, currently, of two boot levels, 0 and 1.
        The idea is to first boot the service at level 0.
        At level 1 services can link to other services required for the functionality of the service.
        Also apps could connect to services during bootService(1), however, the app itself should boot at self.boot()
        After boot level 1 is done, all services should be ready for the Apps booting.'''
        
        pass
    
    def boot(self):
        '''Final boot sequence

        For booting apps.
        Boot is the method to initialize the app rather than self.__init__. 
        In boot the app has access to all services and apps, in self.__init__ and bootService(0) not. 
        This method should be overloaded.'''

        pass

    def halt(self):
        '''Process halt function

        Is called when Radenium closes down.
        This method should be overloade.'''

        pass
