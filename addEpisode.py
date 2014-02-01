#!/usr/bin/env python2
# does some magic fu to read id3 tags from an episode and adds them to the 
# database. 

import MySQLdb as mdb
import ConfigParser
import sys 
import subprocess
import xml.etree.ElementTree as ET
import re
from datetime import datetime

config = ConfigParser.ConfigParser() 
config.read(sys.argv[1]) 

filename=sys.argv[2]

xml=subprocess.check_output(['mediainfo', filename, '--output=XML'])

root = ET.fromstring(xml) 


#Regex for parsing time. 
t_re=re.compile("(.{1,2})mn (.{1,2})s")

time = "" 
link=""
series=""
title=""
creator=""
comment=""


for tag in root[0][0]: 
  if tag.tag == "Complete_name": 
    link=tag.text
  elif tag.tag == "Album": 
    series=tag.text
  elif tag.tag == "Track_name":
    title=tag.text
  elif tag.tag == "Performer": 
    creator=tag.text
  elif tag.tag == "Comment": 
    comment=tag.text
  elif tag.tag == "Duration": 
    print tag.text
    len = t_re.search(tag.text)
    time = int(len.group(1)) * 60 + int(len.group(2)) 

pubdate=datetime.now().strftime("%a, %d %b %Y %H:%M:%S EST")

#Add some more info to the comment. 
comment+= ". " + creator + ". Part of the series: \"" + series + "\"." 


con = mdb.connect(config.get('database', 'host'), 
                  config.get('database', 'user'),
                  config.get('database', 'password'), 
                  config.get('database', 'database'))

with con: 
  cur = con.cursor(mdb.cursors.DictCursor)
  table = config.get('database', 'table')
  cur.execute("insert into sermons(title, link, pubdate, creator, " + 
              "series, description, shortDesc, length) values(%s, %s, " + 
              "%s, %s, %s, %s, %s, %s);", 
              (title, link, pubdate, creator, series, comment, comment, time))
                                                       
