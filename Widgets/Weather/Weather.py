
from Core.Widget import Widget

import urllib.request

class Weather(Widget):
    def bootService(self, level):
        if level==0:
            self.setTitle("Settings")
            self.setDescription("Manage SocialHome settings.")
            self.feeds=['http://feeds.feedburner.com/Filmtotaal-FilmsOpTv']
            self._widgethtml = '''<h2>Buien Radar</h2><div><a href="https://www.buienradar.nl" target="_blank"><img border="0" src="https://image.buienradar.nl/2.0/image/single/RadarMapRainNL?height=512&width=500&renderBackground=True&renderBranding=True&renderText=True"></a>'''
            
            with urllib.request.urlopen(self.feeds[0]) as url:
                s = url.read()
                # I'm guessing this would output the html source code ?
                print(s)

    def renderWidget(self, type="html"):
        return self._widgethtml



