try:
    import datetime
except:
    from Modules.datetime import datetime

from Core.Service import Service

class Debug(Service):
    def bootService(self,level):
        if level==0:
            self.setTitle("Debug Service")
            self.setDescription("Usage: self.process()['Service.Debug'].log('Whatever you want...')")

    def log(self, log, type="INFO"):
        print("RADENIUM-"+str(type)+"> "+str(datetime.datetime.now())+" :"+str(log))
