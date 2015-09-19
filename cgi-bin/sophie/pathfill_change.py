__author__ = "sophiesu"
__date__ = "$14-Aug-2015 10:25:10 AM$"

## THIS FILE ONLY CHANGES THE FILL UNDER THE SHAPE TAG\

if __name__ == "__main__":
    
    import xml.etree.cElementTree as ET
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    tree = ET.ElementTree(file='C:/Users/tzhou/Documents/sophie/Flower.svg')  ##TO SOPHIE: SET THIS TO THE FILE LOCATION OF YOUR SVG\
    tree.getroot()
        
for elem in tree.iterfind('\{http://www.w3.org/2000/svg\}g[@id="Shape"]'):
    #print elem.tag, elem.attrib, elem[0].attrib\
    for child in elem:
        for child2 in child:
            child2.set ('fill','color')    #SET COLOR TO WHAT YOU WANT THE FILL TO BE\
            
#import sys\
tree.write('output.svg')}