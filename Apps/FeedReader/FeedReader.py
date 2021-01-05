
from Core.App import App

try:
    import urllib.request
except:
    pass

class FeedReader(App):
    def boot(self):
        self.setTitle("Feed Reader")
        self.setDescription("Read RSS Feeds")
        self.ui.addElement("text", "feedurl", 'http://feeds.feedburner.com/Filmtotaal-FilmsOpTv', "Provide Feed", "")
        self.ui.addElement("button", "read", '', "Read Feed", "")
        self.feedtext=''



    def renderAppView(self, view, query, post):
        return super().renderAppView(view, query, post) + str(self.feedtext)

    def onButtonPressed(self, button):
        if button == "read":
            try:
                with urllib.request.urlopen(self.ui.getVal("feedurl")) as url:
                    self.feedtext = url.read()
            except:
                pass
