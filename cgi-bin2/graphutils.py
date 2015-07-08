#!/usr/bin/python

import pysam
import matplotlib.pyplot as plt
import urllib2
import json
import gd

#def retrieve_json

#geneid = raw_input("Please enter gene id: ")
#print geneid
geneid = "At1g11190"
print "Looking up %s" %geneid
j = json.loads(urllib2.urlopen("http://bar.utoronto.ca/webservices/araport/gff/get_tair10_gff.php?locus=" + geneid).read())
print j
start = j[u'result'][0][u'start'] if j[u'result'][0][u'strand'] == u'+' else j[u'result'][0][u'end']
end = j[u'result'][0][u'end'] if j[u'result'][0][u'strand'] == u'+' else j[u'result'][0][u'start']
chromosome = int(j[u'result'][0][u'chromosome'])

for region in j[u'result']:
    if region[u'strand'] == u'+':
        if region[u'start'] < start:
            start = region[u'start']
        if region[u'end'] > end:
            end = region[u'end']
    else:
        if region[u'start'] < start:
            start = region[u'start']
        if region[u'end'] > end:
            end = region[u'end']

url = "http://newland.iplantcollaborative.org/iplant/home/araport/rnaseq_bam/aerial/ERR274310/accepted_hits.bam"
xvalues = []
values = []
print "Chr%s:%s-%s" %(chromosome, start, end)
for read in pysam.mpileup(url, "-r", "Chr%s:%s-%s" %(chromosome, start, end)): 
    xvalues.append(float(read.split('\t')[1]))
    values.append(float(int(read.split('\t')[3]) - read.split('\t')[4].count('<') - read.split('\t')[4].count('>')))

values = [int(x / max(values) * 200) for x in values]

rnaseqgraph = gd.image((200, 200))
white = rnaseqgraph.colorAllocate((255,255,255))
black = rnaseqgraph.colorAllocate((0,0,0))
for i in range(len(xvalues)):
    rnaseqgraph.rectangle((int(float(xvalues[i] - start) /(end-start) * 200), 200), (int(float(xvalues[i] - start)/(end-start) * 200), 200 - values[i]), black)        

f = open("rnaseqgraph.png", "w")
rnaseqgraph.writePng(f)
f.close()



exongraph = gd.image((200, 100))
white = exongraph.colorAllocate((255,255,255))
black = exongraph.colorAllocate((0,0,0))
red = exongraph.colorAllocate((255,0,0))
exongraph.lines(((0, 50), (200, 50)), black)
for region in j[u'result']:
    if region[u'type'] == u'exon':
        print (float(region[u'start'] - start) /(end-start), float(region[u'end'] - start)/(end-start))
        exongraph.filledRectangle((int(float(region[u'start'] - start) /(end-start) * 200), 65), (int(float(region[u'end'] - start)/(end-start) * 200), 35), red)        

f = open("test.png", "w")
exongraph.writePng(f)
f.close()