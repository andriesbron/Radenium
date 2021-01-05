
#! DO NOT MODIFY THIS FILE
from Core.Core import Process

class Service(Process):
    '''Root service class
    
    Extends the root process by giving it callback functionality.'''

    def __init__(self, procPointer):
        super().__init__(procPointer)
        self._cbs = []
        self.setTitle("Service")
        self.setDescription("Basic service class to be extended by a service")
        self._triggers=[]
    
    def automator(self):
        return []

    def getTriggers(self):
        return self._triggers

    def getTriggersByType(self, type):
        ts=[]
        for t in self._triggers:
            if t['type'] == type:
                ts.append(t)

        return ts
        
    def bootService(self, level):
        super().bootService(level)

    def iam(self):
        '''Class identifier
        
        Used to identify this class throughout the framework.'''

        return __class__.__name__ +"."+ self.__class__.__name__

    def _callBack(self, event, dataFunc=None):
        '''Call back procedure

        Call it whenever you want to inform subscribers to events happening in your service or app.'''

        for cb in self._cbs:
            cb(event, dataFunc)

    def register(self, func):
        '''Register a callback function in case anything interesting is happening in this service.

        Callback function must comply with:
        method_name(self, event, dataFunc=None)
        event string Indicates what happened
        dataFunc pointer to method that can be called to retrieve event data.'''

        self._cbs.append(func)

    def api(self):
        '''For future purposes. 
        Return json array with available parameters and methods?'''

        return dir(self)

    def attribution(self):
        '''To attribute third party software

        In case a third party library or API is used, you can return a string that will be parsed directly into the settings page. '''
        
        return ""
