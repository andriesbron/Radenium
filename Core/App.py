
#! DO NOT MODIFY THIS FILE
from Core.Service import Service
from Modules.HtmlRenderer.HtmlRenderer import htmlui


class ui_element:
    def __init__(self, type, name, value, lbl, desc, options={}, order=0, placeholder=""):
        '''Initialize the UI
        
        @attention placeholder renders directly into the html view of the element.'''

        self.type=type
        self.name=name
        self.value=value
        self.options=options
        self.lbl=lbl
        self.desc=desc
        self.placeholder=placeholder
        self.min=None
        self.max=None
        
class ui:
    def __init__(self):
        '''
        @attention add logging at app level for now.'''
        self.elements={}
        self._views={}

    def setViewTitle(self, view, title):
        if not view in self._views:
            self._views[view]={'title':title,'layouts':[]}
        else:
            self._views[view]['title']=title

    def addLayout(self, view, layout):
        if not view in self._views:
            self._views[view]={'title':'New View','layouts':[]}
        self._views[view]['layouts'].append(layout)

    def getVal(self, name):
        ''' Get the value of a UI element.

        Returns None if the value is not available which can happen with select elements. For example, a serial port is stored as list, however, it got closed somehow.'''

        if self.elements[name].type == "select":
            if str(self.elements[name].value) in self.elements[name].options['options']:
                return self.elements[name].options['options'][str(self.elements[name].value)]
            else:
                return None

        return self.elements[name].value

    def setVal(self, element, value):
        #@todo make static for value checks.
        #@todo check in setVal for ints or floats limits based on how the min and the max is specified.
        #max = float(self.elements[element].max)
        #min = float(self.elements[element].min)

        if self.elements[element].max == None and self.elements[element].min == None:
            self.elements[element].value = value

        elif self.elements[element].max == None:
            if value >= float(self.elements[element].min):
                self.elements[element].value = value

        elif self.elements[element].min == None:
            if value <= float(self.elements[element].max):
                self.elements[element].value = value
        else:
            if value >= float(self.elements[element].min):
                if value <= float(self.elements[element].max):
                    self.elements[element].value = value

    def setMax(self, element, maxVal):
        self.elements[element].max = maxVal

    def setMin(self, element, minVal):
        self.elements[element].min = minVal

    def addElement(self, type, name, value, lbl, desc, options={}, order=0, placeholder=""):
        if type=='number':
            if not 'step' in options:
                options['step']=1
        elif type=='select':
            if not 'options' in options:
                options['options']={"0":"No Options Given"}

        self.elements[name] = ui_element(type, name, value, lbl, desc, options, order, placeholder)

    def getElement(self, name):
        return self.elements[name]

    def renderUI(self, options={}):
        return htmlui.renderUIForm(self.elements, options['action'])

    def renderUIList(self, elements, options={}):
        #! Renders only a selection of ui elements.
        return htmlui.renderUIForm(elements, options['action'])


class App(Service):
    def __init__(self, procPointer):
        super().__init__(procPointer)
        self.ui=ui()

    def bootService(self,level):
        super().bootService(level)
        if level == 1:
            self.loadUI()

    def saveUI(self, subject, data):
        self.process()['Service.Storage'].save(self.iam(), subject, data)
        #! @todo

    def loadUI(self):
        ui=self.process()['Service.Storage'].retrieve(self.iam(), 'ui')
        self.log(ui)

    def menuLink(self):
        return {"relUrl": "/?App="+self.__class__.__name__, "title":self.getTitle()}

    def onValueChanged(self, input, oldVal, newVal):
        #self.ui.elements[input].value = newVal
        pass

    def onButtonPressed(self, button):
        pass

    def renderAppModules(self, position, request):
        '''Renders app specific for particular template positions.
        Current available positions: bottom'''
        if position == "attribution":
            return self.attribution()

        return ""

    @staticmethod
    def renderAppMenu(baseurl, views):
        viewMenu = ""
        #return str(views)
        for v in views:
            for l in views[v]['layouts']:
                viewMenu += '<a class="btn btn-primary" href="'+baseurl+'&view='+v+'&layout='+l['name']+'">'+l['title']+'</a> '
        return viewMenu

    def renderAppView(self, view, query, post):
        '''@todo ui is now assumed to be a html ui, maybe add UI settings dict or so or use settings app, and provide the ui config dict for rendering.
        Multi ui should be possible eventually. '''
        return '<div>%s</div>'%(self.ui.renderUI({'action':self.menuLink()['relUrl']}))

    def _renderResponse(self, query, post):
        attr =  self.renderAppModules("attribution",post)
        attr = '<h2>Attribution</h2><hr>' + attr if attr != "" else ""
        if 'view' in query:
            view= query['view']
        else:
            view='default'
            
        return {"response":"""<div>%s</div><div>%s</div><div>%s</div>""" %(
            self.renderAppMenu('/?App='+self.__class__.__name__, self.ui._views),
            self.renderAppView(view, query, post),
            attr
            ), "Content-Type":"text/html"}

    def getHttpRequest(self, query, post=False):
        '''Handles the http request for an app. 

        First checks on changes in value of the UI elements and performs call backs.
        Finally renders a default layout, a title, a description and a form layout of the UI.
        For customizations, either overload this method or the renderResponse method.
        
        The handling is very basic, not perfect, however as follows:
        Values and button presses are checked for changes and presses. 
        Whatever is changed is followed by a call on the onValueChanged method using the new value, whatever pressed, onButtonPressed.
        After the call, the new value is stored to the UI element.
        During the event call, both the old value and the new value are available, the new through the event, the old as the current UI element value.'''
        if post != False:
            for var in post:
                if var in self.ui.elements:
                    oldval=self.ui.elements[var].value
                    self.ui.elements[var].value = post[var]
                    if oldval != post[var]:
                        self.onValueChanged(var, self.ui.elements[var].value, post[var])

                    elif self.ui.elements[var].type == "button":
                        self.onButtonPressed(var)

                    # @todo @bug I set here input value, however, if inputs are bound to max sizes, i must respect that, so, I should use setVal and check in setVal for ints or floats limits.
                    #self.ui.elements[var].value = post[var]

        return self._renderResponse(query, post)

    def iam(self):
        '''Class identifier
        
        Used to identify this class throughout the framework.'''

        return __class__.__name__ +"."+ self.__class__.__name__

    def halt(self):
        self.saveUI("ui", {'elements':[]})
        super().halt()
