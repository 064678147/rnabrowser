from flask import Flask
from flask import render_template
import xml.etree.ElementTree


app = Flask(__name__)

# class Record:
#   def __init__(self, file):
#     self.description = file.attrib.get("description")
#     self.experimentno = file.attrib.get("experimentno")
#     self.foreground = file.attrib.get("foreground")
#     self.name = file.attrib.get("name")
#     self.numberofreads = file.attrib.get("numberofreads")
#     self.publicationid = file.attrib.get("publicationid")
#     self.subunitname = file.attrib.get("subunitname")
#     self.title = file.attrib.get("title")
#     self.url = file.attrib.get("url")
#     self.control = file.find("control")


@app.route('/display')
def index():
  e = xml.etree.ElementTree.parse('data/bamdata.xml')
  colour = False
  headers = list(e.getroot()[0].attrib.keys())
  headers.sort()
  current_group = [exp.text for exp in e.getroot()[0].find("groupwith").findall("experiment")]
  xmltable = []
  for file in e.getroot():
    if [exp.text for exp in file.find("groupwith").findall("experiment")] != current_group:
      colour = not colour
      current_group = [exp.text for exp in file.find("groupwith").findall("experiment")]
    entry = file
    entry.attrib['colour'] = "#d3d3d3" if colour else "white"
    entry.attrib["subunitname"] = open("SVGs/" + entry.attrib["svgname"][4:], "r").read()
    xmltable.append(entry)
  return render_template('index.html', xmltableheaders=headers, xmltable=xmltable)

if __name__ == '__main__':
    app.run(debug=True)