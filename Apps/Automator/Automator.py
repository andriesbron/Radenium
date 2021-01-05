
from Core.App import App

class Automator(App):
    def boot(self):
        self.setTitle("Automator")
        self.setDescription("Automate whatever you can.")
        self.someAutomation=False
        for app in self.process():
            auto=self.process()[app].automator()
            if len(auto) > 0:
                self.log(app+" has automator functionality: "+str(auto))
                for form in auto:
                    self.ui.addLayout(app, {'name':form['name'],'title':form['title']})
                    self.someAutomation=True

                self.ui.setViewTitle(app, self.process()[app].getTitle())

        self.ui.setViewTitle('automate', 'Select Automation Service')

    def renderAppView(self, view, query, post):
        self.log(self.iam()+'-renderAppView view='+view)
        self.log(post)
        self.log(query)
        if view != 'default':
            try:
                return str(self.process()[view].automator())
            except:
                pass

        if not self.someAutomation:
            self.process()['Service.UserAlerts'].alert('There are no services or apps instantiated that provide Automation.', 'error')

        return super().renderAppView(view, query, post)
