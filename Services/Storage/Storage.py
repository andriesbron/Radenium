
try:
    import pycom
    import ujson
    #from Core.uos import uos as os
    DISK_ROOT=''
    _PLATFORM_ = 'ESP32'

except:
    import os
    import json
    DISK_ROOT='Services/Storage/Disk/'
    _PLATFORM_ = 'PC'

from Core.Service import Service

class Storage(Service):
    def bootService(self,level):
        if level==0:
            self.setTitle("Storage service for applications")
            self.log("Storage platform "+_PLATFORM_)

    def save(self, identifier, subject, data):
        '''Saves data to disk

        Data is stored using the identifier name. Preferably use app or service name (self.iam())
        '''

        filepath = DISK_ROOT+identifier+'/'+subject
        try:
            if _PLATFORM_ == "PC":
                os.makedirs(filepath)
            elif _PLATFORM_ == "ESP32":
                print("Todo saving stuff")

            with open(filepath + "/data.json", 'w') as output:
                output.write(json.dumps(data))
        except:
            pass

    def retrieve(self, identifier, subject):
        '''Retrieves data from disk

        Data is retrieved using the identifier name. Preferably use app or service name (self.iam())'''

        filepath = DISK_ROOT+identifier+'/'+subject
        try:
            if _PLATFORM_ == "PC":
                with open(filepath + "/data.json", 'r') as input:
                    data=input.read()

                return json.loads(data)
            elif _PLATFORM_ == "ESP32":
                print("Todo getting stuff")
        except:
            pass

        return "Retrieve data failed for: "+subject
