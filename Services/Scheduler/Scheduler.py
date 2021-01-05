
from Core.Service import Service
try:
    import json
    import datetime
    import urllib.request
except:
    import ujson
    from Modules.datetime import datetime
    #from Modules.request import urllib.request

class Scheduler(Service):
    def __init__(self,procPointer):
        super().__init__(procPointer)
        self.setTitle("Scheduler")
        self.setDescription("Trigger and event scheduler.")
        self.setTick(1) #! Service pace per second.
        self._now = datetime.datetime.now()
        self._schedules=[]
        self._sunApiUrl='https://api.sunrise-sunset.org/'
        self._latLongApiUrl='https://nominatim.openstreetmap.org/search'
        self._city='Amsterdam'
        self._sunset=None
        self._sunrise=None
        self._sunrisen=False
        self._sunsetted=False

    def automator(self):
        return [{'notes':'this is the abstraction of a method of this class, so, one parameter should be the pointer to the method called by the automator.','name':'scheduletrigger', 'title':'Schedule a trigger.','par':[
            {'label':'Date and time', 'type':'calendar','name':'datetime'},
            {'label':'Trigger', 'type':'trigger', 'name':'trigg'}
        ]}]

    def _getSunSetRiseUrl(self, lat, lon, format='json'):
        return self._sunApiUrl+ format+'?lat='+lat+'&lng='+lon

    def _getLatLongUrl(self, city, address=' ', format='json'):
        '''https://nominatim.org/release-docs/develop/api/Search/'''
        return self._latLongApiUrl + '?q='+'addressdetails=0&q=street+in+'+city+'&format=json&limit=1'

    def scheduleTrigger(self, datetime, trigger):
        #! format {"event":"[class identifier].whatever", "alarm":"yy-mm-dd hh:mm:ss"}
        self._schedules.append({"alarm":datetime, "event":trigger, "trig":False})

        return True

    def getSunSetAndRise(self, city):
        '''Gets the sunset and sunrise by city

        Take notice, that is based on the timezone from which you query.
        So, on the other side of your world, sunrise might occur at noon, that's the idea and that's how we do it.'''

        try:
            #! first get the lat long
            with urllib.request.urlopen(self._getLatLongUrl(city)) as url:
                apicall = json.loads(url.read())[0]
                self.log(self._city+' '+str(apicall['lat'])+','+str(apicall['lon']))

            #! @todo Other option is php system call, e.g. echo(date_sunset(time(),SUNFUNCS_RET_STRING,38.4,-9,90,1));
            with urllib.request.urlopen(self._getSunSetRiseUrl(apicall['lat'],apicall['lon'])) as url:
                apicall = url.read()

            return json.loads(apicall)['results']
        except:
            pass
            return False

    def tick(self):
        self._now = datetime.datetime.now()
        for sched in self._schedules:
            if not sched['trig']:
                dt=self.parseDateTimeString(sched['alarm'])
                if self._now > datetime.datetime(dt[0][0], dt[0][1], dt[0][2],dt[1][0],dt[1][1],dt[1][2]):
                    self._callBack(sched['event'])
                    self.log('Trigger-'+sched['event']+'!')
                    sched['trig']=True

        self._runSunRiseAndSet()

    def _runSunRiseAndSet(self):
        sunrise = self._now.replace(hour=int(self._sunrise[0]), minute=int(self._sunrise[1]), second=int(self._sunrise[2]), microsecond=0)
        sunset = self._now.replace(hour=int(self._sunset[0])+12, minute=int(self._sunset[1]), second=int(self._sunset[2]), microsecond=0)
        if not self._sunrisen and self._now < sunset:
            if self._now > sunrise:
                self._sunrisen = True
                self._sunsetted = False
                self._callBack(self.iam()+'.sunrise.now')
                self.log('Good day '+self._city+'!')

        elif not self._sunsetted and self._now > sunset:
            self._sunrisen = False
            self._sunsetted = True
            self._callBack(self.iam()+'.sunset.now')
            self.log('Good night '+self._city+'!')

        if (self.isItDay()):
            self._callBack(self.iam()+'.it.is.day')
        else:
            self._callBack(self.iam()+'.it.is.night')

    def trigger(self, trig):
        pass
        #! Schedule the trigger.



    def isItDay(self):
        return self._sunrisen and not self._sunsetted

    def parseDateTimeString(self, dtstr):
        dt = dtstr.split(' ')
        return [dt[0].split('-'), dt[1].split(':')]

    def boot(self):
        #! @todo if city is equal to stored city and sunset and rise is stored as well, don't do an api call.
        self._city = 'Amsterdam' #! Should get it from settings app.
        sun = self.getSunSetAndRise(self._city)
        #! This is short around the corner... the first split index 1 contains AM/PM
        try:
            self._sunrise=sun['sunrise'].split(' ')[0].split(':')
            self._sunset=sun['sunset'].split(' ')[0].split(':')
            #! Initialize scheduler variables
            self._runSunRiseAndSet()
        except:
            pass

    def attribution(self):
        '''Attribution
        For getting Lat Long coordinates: https://operations.osmfoundation.org/policies/nominatim/
        For getting sunset and sunrise times: https://api.sunrise-sunset.org/'''

        return '''Service.Scheduler makes use of <a href="https://nominatim.org">Nominatum lat long look up</a> and <a href="https://sunrise-sunset.org/">sunrise-sunset api</a>.</div>'''
