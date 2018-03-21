#!/usr/bin/python
import tempfile
import cups
import cgi
import cgitb; cgitb.enable()

class ZebraLabel(object):
    width = 0
    height = 0
    labels_per_line = 1
    darkness = 30
    label_home = (0,0)
    print_rate = ('A','C','C')
    fields = None
    font = None
    # all of the dimensions are in pixels.  For GX430t this is 300 dpi so 600 = 2 inches
    def __init__(self,width=600,height=226,labels_per_line=1):
        self.width = width
        self.height = height
        self.labels_per_line = labels_per_line
        self.fields = list()
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        output = list()
        output.append(self._header())
        output.append(self._footer())
        return ''.join(output)
    def _header(self):
        # This makes all the non-printable settings for the printer defining the labels
        output = list()
        output.append('^XA')
        output.append('^LH{0},{1}'.format(*(self.label_home)))
        output.append('^LL{0}'.format(self.height))
        output.append('^PW{0}'.format(self.width))
        output.append('~SD{0}'.format(self.darkness))
        output.append('^PR{0},{1},{2}'.format(*(self.print_rate)))
        return ''.join(output)
    def _footer(self):
        # This ends the label
        return '^XZ'
class RectLabel(ZebraLabel):
    def __init__(self):
        # This defines the label I actually use in lab
        ZebraLabel.__init__(self,width=320,height=188,labels_per_line=1)
    def __str__(self):
        # This returns the string representation of the label including the header and footer
        output = list()
        output.append(ZebraLabel._header(self))
        if self.font:
            for x in self.fields:
                x.font = self.font
                output = output + str(x)
        else:
            output = output + [str(x) for x in self.fields]
        output.append(ZebraLabel._footer(self))
        return ''.join(output)
class ZebraField(object):
    # This object defines a field on the label.  This can be a text field or a barcode if you change the font.
    origin = (0,0) # Position on the label
    font = (0,0,0)
    data = ''
    def __init__(self,data='',origin=(0,0),font=(0,0,0)):
        self.data = data
        self.font = font
        self.origin = origin
    def __str__(self):
        output = list()
        
        if self.font[1] > 0 and self.font[2] > 0:
            output.append('^CF{0},{1},{2}'.format(*(self.font)))
        elif self.font[1] > 0:
            output.append('^CF{0[0]},{0[1]}'.format(self.font))
        elif self.font[2] > 0:
            output.append('^CF{0[0]},,{0[2]}'.format(self.font))
        else:
            output.append('^CF{0[0]}'.format(self.font))
            
        output.append('^FO{0},{1}'.format(*(self.origin)))
        output.append('^FD{0}^FS'.format(self.data))
        return ''.join(output)
def webpage(in_form):
    # This generates the form for the webpage that you can fill in
    print "Content-type: text/html"
    print
    print """
        <html>
        <head><title>Label printer</title></head>
        <body>
            <h3>Rectangle Label Printer</h3>
            <p>Entry blank</p>
            <form method="post" action="lpr.py">
                <p>Line 1:<input type="text" name="line1" value="{0}"/></p>
                <p>Line 2:<input type="text" name="line2" value="{1}"/></p>
                <p>Line 3:<input type="text" name="line3" value="{2}"/></p>
                <p>Line 4:<input type="text" name="line4" value="{3}"/></p>
                <p>Or copy and paste from Excel:<textarea name="label" rows="4" cols="50">{4}</textarea></p>
                <p><input type="submit" value="Print"/></p>
            </form>
        </body>
        </html>
    """.format(in_form["line1"],in_form["line2"],in_form["line3"],in_form["line4"],in_form["label"])
def main():
    form = cgi.FieldStorage()
    formdict = dict()
    formdict["line1"] = "" if "line1" not in form else form.getvalue("line1")
    formdict["line2"] = "" if "line2" not in form else form.getvalue("line2")
    formdict["line3"] = "" if "line3" not in form else form.getvalue("line3")
    formdict["line4"] = "" if "line4" not in form else form.getvalue("line4")
    formdict["label"] = "" if "label" not in form else form.getvalue("label")
    webpage(formdict)
    if "line1" in form:
        # if we have the lines filled in it will generate a label and a 4 lines of fields
        label = RectLabel()
        label.fields.append(ZebraField(form.getvalue("line1",""),(20,20),(0,34,0)))
        label.fields.append(ZebraField(form.getvalue("line2",""),(20,57),(0,34,0)))
        label.fields.append(ZebraField(form.getvalue("line3",""),(20,94),(0,34,0)))
        label.fields.append(ZebraField(form.getvalue("line4",""),(20,131),(0,34,0)))
        # Then it will try to save a temporary file with the ZPL in it
        try:
            temp_label = tempfile.NamedTemporaryFile('w+b',delete=False)
            temp_label.write(str(label))
            temp_label.close()
        except IOError:
            pass
#        print temp_labelo
        # Finally, connect to the printer and send the ZPL to print it out
        c = cups.Connection(host="vogt1005.scripps.edu")
#	print c.getPrinters()
        c.printFile("Zebra", temp_label.name, "ZPL", dict())
    if "label" in form:
        # if you fill in the cut and paste part it will make a label from each line
        labeldata = form.getvalue("label","")
        labels = labeldata.splitlines()
        for labelline in labels:
            label = RectLabel()
            labelfields = labelline.split('\t')
            label.fields.append(ZebraField(labelfields[0],(20,20),(0,34,0)))
            if len(labelfields) > 1:
                label.fields.append(ZebraField(labelfields[1],(20,57),(0,34,0)))
            if len(labelfields) > 2:
                label.fields.append(ZebraField(labelfields[2],(20,94),(0,34,0)))
            if len(labelfields) > 3:
                label.fields.append(ZebraField(labelfields[3],(20,131),(0,34,0)))

            try:
                temp_label = tempfile.NamedTemporaryFile('w+b',delete=False)
                temp_label.write(str(label))
                temp_label.close()
            except IOError:
                pass
#            print temp_label
            c = cups.Connection(host="vogt1005.scripps.edu")
#            print c.getPrinters()
            c.printFile("Zebra", temp_label.name, "ZPL", dict())
 
if __name__ == '__main__':
    main()
