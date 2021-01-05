class HtmlRenderer:
    def __init__(self):
        pass

class htmlui:
    '''@todo should be class htmluiform'''
    ELEMENT_TYPES=["indicator", "number", "text", "button", "submit", "datetime-local", "select", "range",        "bar", "textarea","hidden","email", "password","color","checkbox","file","month","search","tel", "week"]
    @staticmethod
    def render(element):
        ren = ""
        if element.type == "text":
            ren = htmlui.renderText(element)
        elif element.type=='button':
            ren = htmlui.renderButton(element)
        elif element.type == "select":
            ren = htmlui.renderSelect(element)
        elif element.type == "indicator":
            ren = htmlui.renderIndicator(element)
        elif element.type =="number":
            ren =htmlui.renderNumber(element)
        elif element.type =="datetime":
            ren =htmlui.renderNumber(element)
        else:
            ren = "<input class=\"form-control\" name=\""+element.name+"\" type=\""+element.type+"\" value=\""+str(element.value)+"\" />"

        if ren != "":
            return "<div class=\"form-controls\"><span class=\"control-label\"><label for=\"" + element.name+"\">" + element.lbl+"</label></span><span>" + ren +"</span></div>"

    @staticmethod
    def renderRange(element):
        return "<input type=\"range\" id=\""+element.name+"\" name=\""+element.name+"\" min=\"id=\""+element.min+"\"\" max=\"id=\""+element.max+"\"\" />"

    @staticmethod
    def renderDatetime(element):
        return "<input type=\"datetime-local\" id=\""+element.name+"\" name=\""+element.name+"\">"

    @staticmethod
    def renderButton(element):
        return "<button id=\""+element.name+"\" class=\"form-control\" name=\""+element.name+"\" type=\"submit\" value=\""+str(element.value)+"\" />"+element.lbl+"</button>"

    @staticmethod
    def renderNumber(element):
        return "<input class=\"form-control\" id=\""+element.name+"\" name=\""+element.name+"\" type=\"number\" min=\"id=\""+element.min+"\"\" max=\"id=\""+element.max+"\"\" step=\""+element.options['step']+"\" value=\""+str(element.value)+"\" />"

    @staticmethod
    def renderIndicator(element):
        table=""
        minmax = ""
        if element.min != None:
            minmax = "Min: " + str(element.min)

        if element.max != None:
            minmax += " Max: " + str(element.max)

        table += "<tr class=\"form-ui-indicator\"><td>"+element.lbl + "</td><td>&nbsp;</td><td>" + str(element.value)+" "+ minmax +"</td></tr>\n"
        return "<div class=\"form-ui-indicator\"><table>"+table+"</table></div>"

    @staticmethod
    def renderSelect(element):
        options = ""
        for opt in element.options['options']:
            selected = ""
            if str(opt) == str(element.value):
                selected = "selected "
            options += "<option "+selected+"value=\""+opt+"\">"+element.options['options'][opt]+"</option>"

        return  "<select id=\""+element.name+"\" class=\"form-control\" value=\""+str(element.value)+"\" name=\""+element.name+"\">"+options+"</select>"

    @staticmethod
    def renderText(element):
        return  "<input id=\""+element.name+"\" class=\"form-control\" name=\""+element.name+"\" type=\""+element.type+"\" value=\""+str(element.value)+"\" placeholder=\""+element.placeholder+"\"/>"

    @staticmethod
    def renderUIForm(elements,action):
        html = htmlui.renderUserDisplay(elements)

        return html + "<form action=\""+action+"\" method=\"post\">" + htmlui.renderUserInput(elements) + "<div>&nbsp;</div></form>"

    @staticmethod
    def renderUserDisplay(elements):
        html=""
        for el in elements:
            if elements[el].type == "indicator":
                minmax = ""
                if elements[el].min != None:
                    minmax = "Min: " + str(elements[el].min)

                if elements[el].max != None:
                    minmax += " Max: " + str(elements[el].max)

                html += "<tr class=\"form-ui-indicator\"><td>"+elements[el].lbl + "</td><td>&nbsp;</td><td>" + str(elements[el].value)+" "+ minmax +"</td></tr>\n"

        if html != "":
            html="<table>"+html+"</table>"

        return "<div class=\"form-ui-indicator\">"+html+"</div>"

    @staticmethod
    def renderUserInput(elements):
        #! @todo don't render indicators!
        html = ""
        for el in elements:
            if elements[el].type != 'indicator':
                html += "<div>"+htmlui.render(elements[el])+"</div>\n"

        return html
