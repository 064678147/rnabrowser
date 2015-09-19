from xml.etree.ElementTree import *

tree = parse("cgi-bin/data/bamlocator2.xml")
container = tree.findall("file")
data = []
for elem in container:
    key = elem.attrib["experimentno"]
    data.append((key, elem))
data.sort()
container[:] = [item[-1] for item in data]
tree.write("test.xml")