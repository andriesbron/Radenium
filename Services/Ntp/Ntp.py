
from Core.Service import Service
#from Services.Ntp import untplib


from contextlib import closing
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import time

NTP_PACKET_FORMAT = "!12I"
NTP_DELTA = 2208988800  # 1970-01-01 00:00:00
NTP_QUERY = b'\x1b' + 47 * b'\0'  

class Ntp(Service):

    def bootService(self,level):
        if level==0:
            self.log(time.ctime(self.ntp_time()).replace("  ", " "))

    def ntp_time(self, host="pool.ntp.org", port=123):
        with closing(socket( AF_INET, SOCK_DGRAM)) as s:
            s.sendto(NTP_QUERY, (host, port))
            #msg, address = s.recvfrom(1024)
            #msg, address = s.recvfrom(48)
            try:
                msg, address = s.recvfrom(1)
                print(msg)
                unpacked = struct.unpack(NTP_PACKET_FORMAT,
                msg[0:struct.calcsize(NTP_PACKET_FORMAT)])
                
                return unpacked[10] + float(unpacked[11]) / 2**32 - NTP_DELTA

            except:
                pass
            

    def _bootService(self, level):
        if level==0:
            c=untplib.NTPClient()
            resp=c.request('0.uk.pool.ntp.org', version=3, port=123)
            print("Offset is ", resp.offset)
            try:
                from machine import RTC
                import time
                rtc = RTC()
                print("Adjusting clock by ", resp.offset, "seconds")
                rtc.init(time.localtime(time.time() + resp.offset))
            except:
                pass


