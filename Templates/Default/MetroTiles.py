__metro_1__ = '''
<table><tr>
    <td><div class="metro-tile metro-tile-small metro-tile-store"><a href="%s">%s</a></div></td>
    <td><div class="metro-tile metro-tile-small metro-tile-xbox"><a href="%s">%s</a></div></td>
    <td><div class="metro-tile metro-tile-google"><a href="%s">%s</a></div></td>
    <td><div class="metro-tile metro-tile-angrybirds"><a href="%s">%s</a></div></td>
</tr></table>'''

#! Remove all spaces, also spaces take space you know...
__metro_css__ = '''
body {
background: url(https://cssbox.googlecode.com/svn/demo/Windows8MetroTiles/img/Background.jpg) bottom no-repeat;
background-color:58169a;
font-family: sans-serif;
font-size: 12px;
}
#header {
color:#fff;
}
#container {
width:750px;
margin-left:auto;
margin-right:auto;
}
.metro-surface{
padding: 40px 0px 0px 0px;
}
.metro-tile {
background-color: #D8512B;
border-color: #DC6241;
width: 232px;
height: 104px;
padding: 5px;
color: #FFF;
border-width: 3px;
border-style: solid;
cursor: default;
-webkit-transition: 0.1s all;
-moz-transition: 0.1s all;
-ms-transition: 0.1s all;
transition: 0.1s all;
}
.metro-tile-small {
width: 104px;
height: 104px;
}
.metro-tile-store {
background: url(https://cssbox.googlecode.com/svn/demo/Windows8MetroTiles/img/Store.png);
background-color: #2878EC;
border-color: #2878EC;
}
.metro-tile-xbox {
background: url(https://cssbox.googlecode.com/svn/demo/Windows8MetroTiles/img/XBox.png);
background-position: 8px 8px;
background-color:#6CB71E;
border-color:#6CB71E;
}
.metro-tile-google {
background: url(https://cssbox.googlecode.com/svn/demo/Windows8MetroTiles/img/Google.png);
background-color: #009719;
border-color: #009719;
}
.metro-tile-angrybirds {
background: url(https://cssbox.googlecode.com/svn/demo/Windows8MetroTiles/img/AngryBirds.jpg);
border-image: url(https://cssbox.googlecode.com/svn/demo/Windows8MetroTiles/img/AngryBirds.jpg) 1;
border: 2pt solid #cccccc;
color: #ffffff;
}
.metro-tile-angrybirds a {
color: #ffffff;
}
'''

__component__ = '''<div id="component">\n%s\n</div>'''
__menu_link__ = '<a class="menu" href="%s">%s</a>' #! link, name
__header__ = '''<div id="header"><h2>%s</h2></div>'''

#! HTML elements
__html_input__ = '<input name="%s" type="text" value="%s" />'
__html_input_hidden__ = '<input name="%s" type="hidden" value="%s" />'
__html_select__ = '<select name="%s">%s</select>' #%(name, __html_select_option__ )
__html_select_option__ = '<option %s value="%s">%s</option>' # %("selected", value, description)


__html__ = '<html><header><style>%s</style></header><body>%s\n%s\n%s\n</body></html>'


class MetroTiles:
    def __init__( self ):
        self.header = "Radenium IOT"
        self.menu = ""
        self.component = ""
        
    def setView( self, com, view, data={} ):
        if view == "uiform":
            self.view_uiform( com, data )
        elif view == "notification":
            self.view_notification( com, data )
        elif view == "blunt":
            self.view_blunt( com, data )
        else:
            self.view_home( data )
        
        
    def setMenu( self, menu ):
        pass
        
        
    def view_home( self, menu={} ):
        #! Putting the Tiles into the menu... my o my...
        row=0
        col=0
        total = 4
        columns = []
        rows = []
        for m in menu:
            columns.append(m)
            col += 1
            if col%4 == 0:
                total += 4
                rows.append(columns)
                columns = []
        
        while col < total: #! Add up all the rows
            columns.append( { 'com':'', 'name':'Home' } )
            col += 1
            
        rows.append(columns)
        self.menu = ''
        for row in rows:
            print( row )
            self.menu += __metro_1__ % ( '/?com='+str(row[0]['com']), str(row[0]['name']),'/?com='+str(row[1]['com']), str(row[1]['name']),'/?com='+str(row[2]['com']), str(row[2]['name']),'/?com='+str(row[3]['com']), str(row[3]['name']) )
        
        
    def view_blunt( self, com, data ):
        self.component = __component__%( "<p>Blunt data dump because of not setting an existing view</p>" + str(data) )
        
        
    def view_notification( self, com, data ):
        self.component = __component__%(str(data))
        
        
    def view_uiform( self, com, data ):
        self.component = '\n<form action="" method="GET">\n'
        self.component += '<table>\n'
        
        for p in data:
            self.component += '<tr>'
            if p["type"] == "text":

                self.component += '<td>'+p["name"] + '</td><td>' + __html_input__%(str(p["id"]), "" ) + '</td>'
                
            elif p["type"] == "select":
                options = ""
                try:
                    for key in p["options"]:
                        options += __html_select_option__%("", str(p["options"][key]),str(key)) + "\n" # selected, name, value
                
                    self.component += '<td>' + str(p["name"]) + '</td><td>' + __html_select__%(str(p["id"]), options) + '</td>'
                
                except:
                    print("template.py: An error in view_uiform > options")
            
            self.component += '</tr>\n'
            
        self.component += '</table>\n'
        
        for phid in data:
            if phid["type"] == "hidden":
                self.component += __html_input_hidden__%( str(phid["id"]), str(phid["value"]) )

        self.component += __html_input_hidden__%("com", str(com) )
        self.component += '<input type="submit" value="Submit">\n'
        self.component += '</form>\n'
        
        
    def html( self ):
        #html = '<html><header><style>'+__metro_css__+'</style></header><body>'+__metro_1__ + self.menu + self.component + '</body></html>'
        #html = __html__%(__metro_css__,__metro_1__,self.menu,self.component)
        html = '<html><header><style>'
        html += __metro_css__ 
        html += '</style></header><body><div id="container">'
        html += __header__%str( self.header )
        html += str( self.menu )
        try:
            html += str( self.component )
        except:
            html += "Could not concatenate component string. Did you use something like __component__%(self_component)?"
        
        #html += __component__%( str( self.component ) )
        self.component = '' #! Reset component view
        html += '</div></body></html>'
        
        
        return html
        
        