from flask import Flask, request
from flask import render_template
import xml.etree.ElementTree
import multi

HOST = "127.0.0.1"
PORT = 5000

app = Flask(__name__)


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

@app.route('/')
def uiviewer():
  print render_template('uiview.html')

@app.route('/multi')
def multiview():
  return multi.run(request.args.get('locus'))
  
if __name__ == '__main__':
  print "Listening on " + HOST + ":" + str(PORT)
  app.run(host=HOST, port=PORT, debug=True)
