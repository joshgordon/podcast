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
config.read("config.ini") 

filename=sys.argv[1]

xml=subprocess.check_output(['mediainfo', filename, '--output=XML'])

root = ET.fromstring(xml) 


#get the time. 
t_re=re.compile("(..)mn (..)s")
len = t_re.search(root[0][1][3].text)
time = int(len.group(1)) * 60 + int(len.group(2)) 

link=root[0][0][0].text
series=root[0][0][6].text
title=root[0][0][7].text
creator=root[0][0][9].text
comment=root[0][0][14].text
pubdate=datetime.now().strftime("%a, %d %b %Y %H:%M:%S EST")


con = mdb.connect(config.get('database', 'host'), 
                  config.get('database', 'user'),
                  config.get('database', 'password'), 
                  config.get('database', 'database'))

with con: 
  cur = con.cursor(mdb.cursors.DictCursor)
  table = config.get('database', 'tabe')
  cur.execute("insert into " + table + "(title, link, pubdate, creator, " + 
              "series, description, shortDesc, length) values('%s', '%s', " + 
              "'%s', '%s', '%s', '%s', '%s', '%s');", 
              (title, link, pubdate, creator, series, comment, comment, time))
                                                       
