#!/usr/bin/env python3
"""does some magic fu to read id3 tags from an episode and adds them to the 
database. 

Copyright (C) 2015 Joshua Gordon <github@joshgordon.net>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A copy of the GNU General Public License version 2 can be obtained at 
http://www.gnu.org/licenses/gpl-2.0.html or by writing to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
import pymysql as mdb
import configparser
import sys 
import subprocess
import xml.etree.ElementTree as ET
import re
from datetime import datetime

"""A class that is mostly for the use of containing the config file. """ 
class EpisodeWriter(): 

  """Pass in a path to a config file""" 
  def __init__(self, configFile):
    self.config = configparser.ConfigParser()
    self.config.read(configFile) 

  """Pass in the URL to an MP3 file on the internet.""" 
  def writeEpisode(self, filename): 
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
        print(tag.text)
        len = t_re.search(tag.text)
        time = int(len.group(1)) * 60 + int(len.group(2)) 

    pubdate=datetime.now().strftime("%a, %d %b %Y %H:%M:%S EST")

    #Add some more info to the comment. 
    comment+= ". " + creator + ". Part of the series: \"" + series + "\"." 


    con = mdb.connect(self.config.get('database', 'host'), 
                      self.config.get('database', 'user'),
                      self.config.get('database', 'password'), 
                      self.config.get('database', 'database'))
    
    with con: 
      cur = con.cursor(mdb.cursors.DictCursor)
      table = self.config.get('database', 'table')
      cur.execute("insert into " + table + "(title, link, pubdate, creator, " + 
                  "series, description, shortDesc, length) values(%s, %s, " + 
                  "%s, %s, %s, %s, %s, %s);", 
                  (title, link, pubdate, creator, series, comment, comment, time))

  def checkExistence(self, url):
    con = mdb.connect(self.config.get('database', 'host'), 
                      self.config.get('database', 'user'),
                      self.config.get('database', 'password'), 
                      self.config.get('database', 'database'))

    with con:
      cur = con.cursor(mdb.cursors.DictCursor)
      table = self.config.get('database', 'table')
      cur.execute("select * from " + table + " where link = %s; ", url)
      matches = cur.fetchall()
      if len(matches) > 0:
        return True
      else:
        return False
      

#  We run on our own if we're called directly. 
if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage {} config.ini http://url/of/mp3/file".format(sys.argv[0]))
    sys.exit(1) 
  writer = EpisodeWriter(sys.argv[1])
  writer.writeEpisode(sys.argv[2])
