#!/usr/bin/env python

# kind of a sloppy hack to cram geonames cities data into local-solr

import sys
import codecs
import solr

if len(sys.argv) != 3:
    print "usage: index.py [cities file] [solr url]"
    sys.exit(-1)

# get country/state code lookup table
states = {}
for line in codecs.open('admin1Codes.txt', encoding='utf8'):
    line = line.strip()
    p = line.split("\t")
    if len(p) !=2: 
        continue 
    country_code, state_code= p[0].split('.')
    if states.has_key(country_code):
        states[country_code][state_code] = p[1]
    else:
        states[country_code] = {state_code: p[1]} 

# load and index the cities file
s = solr.SolrConnection(sys.argv[2])
count = 0
for row in codecs.open(sys.argv[1], encoding='utf8'):
    count += 1
    row = row.strip()
    p = row.split("\t")
    alt_name = p[3].split(',')
    doc = {
            'id':p[0], 'name':p[1], 'lat':p[4], 'lng':p[5],
            'country':p[8], 'alt_name':alt_name, 'population':p[14], 
            'elevation':p[15], 'gtopo30':p[16], 'timezone':p[17]
          }

    if p[8] and p[10]:
        doc['state'] = states.get(p[8], {}).get(p[10], None)

    # remove empty values
    for k in doc.keys():
        if not doc[k]:
            doc.pop(k)

    s.add(**doc)

    if count % 1000 == 0:
        s.commit()

    print "[%s] %s %s [%s]" % (count, doc['name'], doc['country'], doc['id'])

s.commit()
