#!/usr/bin/python
print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print "<title>hello world</title>"

import os
import cgi
import cgitb
import re
from HTMLParser import HTMLParser
cgitb.enable()
# import urllib2
# import json
#import gd
# import graphutils
# geneid = "At1g11190"
# j = json.loads(urllib2.urlopen("http://bar.utoronto.ca/webservices/araport/gff/get_tair10_gff.php?locus=" + geneid).read())
# start = j[u'result'][0][u'start'] if j[u'result'][0][u'strand'] == u'+' else j[u'result'][0][u'end']
# end = j[u'result'][0][u'end'] if j[u'result'][0][u'strand'] == u'+' else j[u'result'][0][u'start']
# chromosome = int(j[u'result'][0][u'chromosome'])

# for region in j[u'result']:
#     if region[u'strand'] == u'+':
#         if region[u'start'] < start:
#             start = region[u'start']
#         if region[u'end'] > end:
#             end = region[u'end']
#     else:
#         if region[u'start'] < start:
#             start = region[u'start']
#         if region[u'end'] > end:
#             end = region[u'end']

#url = "http://newland.iplantcollaborative.org/iplant/home/araport/rnaseq_bam/aerial/ERR274310/accepted_hits.bam"
#xvalues = []
#values = []

#for read in pysam.mpileup(url, "-r", "Chr%s:%s-%s" %(chromosome, start, end)): 
    #xvalues.append(float(read.split('\t')[1]))
    #values.append(float(int(read.split('\t')[3]) - read.split('\t')[4].count('<') - read.split('\t')[4].count('>')))

#values = [int(x / max(values) * 200) for x in values]
# create a subclass and override the handler methods
collector = {}

# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
# 		print self.getpos()
# #         if tag == 'g':
			
# # 			collector[attrs] = 
# 		print "Encountered an start tag:", tag
#     def handle_endtag(self, tag):
#         print "Encountered an end tag :", tag
#     def handle_data(self, data):
#         print "Encountered some data  :", data
# parser = MyHTMLParser()
# parser.feed(data)
svg = open("SVGs/youngSeedling.svg", "r")
data = svg.read()

form = cgi.FieldStorage()
print '<script src="sort.js"> </script>'
print '<style>'
print 'td {text-align:center;}'
print '</style>'
print "<body>"
print '	<table border="1" class="sortable" style="width:100%" align="centre">'
print '			<th> Expt </th>'
print '			<th> RNA-Seq Coverage <br /><img src="test.png"> </th>'
print '			<th> eFP - RPKM </th>'
print '			<th> SRA Record </th>'
print '			<th> Details </th>'

files = [ f for f in os.listdir("SVGs") if os.path.isfile(os.path.join("SVGs",f)) ]
for item in files:
	svg = open("SVGs/" + item, "r")
	data = svg.read()
	print '		<tr>'
	print '			<td> WT </td>'
	print '			<td> <img src="rnaseqgraph.png"> </td>'
	print '			<td>' + data.replace('fill="none"', 'fill="blue"') + '</td>'
	print '			<td> <a> SRA12345 </a> </td>'
	print '			<td> <a> See Filichkin et. al 2010 </a> </td>'
	print '		</tr>'
print '	</table>'

print form.getvalue("name")

print "</body>"
# print "</html>"

# look into svg parsing
# populate the fields with svg. try different colours


#cgi.FieldStorage()
#form.getvalue()