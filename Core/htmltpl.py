
#! DO NOT MODIFY THIS FILE

#! Anders doen
#! Ik heb een class met module posities.
#! Die class die extend een html tpl met statics of gewoon een file met {$REFERENCES} die worden vervangen door
#! de template positie content.
#! deze class heeft dus alle module posities, de init krijgt mee welk template er gerendered moet worden.
#! renderen zou met static methods moeten in modules.
#! ala joomla.

class menuitem:
    def __init__(self, name, link, image):
        self.link = link
        self.name = name
        self.image = image

class htmltpl:
    def __init__(self, tpl="Default"):
        self._renderedTime = "not yet implemented"
        self._scripts = []
        self._scriptDeclarations = []
        self._metas = []
        self._bodyArgs=[]
        self._styles=["style/default.css"]
        self._styleDeclarations=[]
        self._component = "No component given"
        self._menuItems = []
        self._notifications = ""
        self._title="Radenium"
        self._description="A tiny smart home hub framework build in Python"

    def setTitle(self, title):
        self._title=title
    def setDescription(self, desc):
        self._description=desc

    def setNotifications(self, notificationHtml):
        self._notifications=notificationHtml

    @staticmethod
    def renderMenuContainer(menuitems):
        menuhtml = ""
        for menu in menuitems:
            menuhtml += "<li class=\"menu-item hidden\"><a href=\"" + menu['relUrl'] + "\">" + menu['title']+"</a></li>\n"

        return """
            <div class=\"menu\">
                <ul>
                    <li class="logo"><a href="/"><img height="44" title="Radenium Logo"
                        alt="Logo!"
                        src="/images/radenium_text_small.png"></a>
                    </li>
                    <li class="menu-toggle"><button onclick="toggleMenu();">&#9776;</button></li>
                    <li class="menu-item hidden"><a href="/">Home</a></li>
                    """ + menuhtml + """
                    <li class="menu-item hidden"><a href="https://www.github.com/andriesbron" target="_blank">GitHub</a></li>
                </ul>
            </div>
            """

    def renderMenu(self):
        return self.renderMenuContainer(self._menuItems)

    def renderContainer(self):
        return """
        <div class=\"container\">
        """ + self._notifications + self._component + """
        </div>
        """


    def renderHero(self):
        return """<div class="heroe">
		<h1>"""+self._title+"""</h1>
		<h2>"""+self._description+"""</h2>
	</div>"""

    @staticmethod
    def renderFooter(variables):
        return """<footer>
	<div class="environment">

		<p>Page rendered in """+variables['rendertime']+""" seconds</p>
	</div>

	<div class="copyrights">
		<p>&copy; 2020 Andries Bron.</p>
	</div>

</footer>"""

    @staticmethod
    def renderHead(title, styles):
        styles = "\" />\n<link rel=\"stylesheet\" href=\"".join(styles)
        head =""
        return """
    <head>
    	<meta charset="UTF-8">
	    <title>"""+title+"""</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link rel="shortcut icon" type="image/png" href="/favicon.ico"/>
        <link rel=\"stylesheet\" href=\"""" + styles +"""\" />""" + head + """
    </head>"""

    def setComponent(self, componentHtml):
        self._component = componentHtml

    #! @todo @staticmethod
    def renderBody(self):
        bodytags =""
        body="""
        <header>
            """ + self.renderMenu() + self.renderHero() + """
        </header>
        <section>
            """ + self.renderContainer() + """
        </section>
            """ + self.renderFooter({'rendertime':self._renderedTime})

        return """
    <body """+bodytags+""">
        """ + body + """
        <script>
	function toggleMenu() {
		var menuItems = document.getElementsByClassName('menu-item');
		for (var i = 0; i < menuItems.length; i++) {
			var menuItem = menuItems[i];
			menuItem.classList.toggle("hidden");
		}
	}
</script>
    </body>"""

    def render(self):
        html=htmltpl.renderHead(self._title, self._styles) + self.renderBody()
        #! Clear the notifications
        self._notifications = ""

        return """<!DOCTYPE html>
            <html>""" + html + """</html>"""


    def addMenu(self, relUrl):
        self._menuItems.append(relUrl)
