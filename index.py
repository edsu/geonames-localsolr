#!/usr/bin/env python

# uses geonames http://download.geonames.org/export/dump/cities1000.zip
# index.py cities.txt http://localhost:8089/solr

import sys
import codecs

import solr

s = solr.SolrConnection(sys.argv[2])
count = 0

for row in codecs.open(sys.argv[1], encoding='utf8'):
    count += 1
    row = row.strip()
    p = row.split("\t")
    id, name, lat, lng, country, state = p[0], p[1], p[4], p[5], p[8], p[10]
    alt_name = p[3].split(',')

    s.add(id=id, name=name, lat=lat, lng=lng, state=state, country=country,
            alt_name=alt_name)
    if count * 1000 == 0:
        s.commit()
    print "[%s] %s %s  %s [%s]" % (count, name, state, country, id)

s.commit()
    


