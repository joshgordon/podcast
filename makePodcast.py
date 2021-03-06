#!/usr/bin/env python3
"""This is a friday-night hack. Please excuse the hackieness. 

Looks in a mysql database for information about urls to publish as a podcast. 
Takes an ini-file as the only argument

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

import configparser
import sys
import os
from datetime import datetime
import pymysql as mdb 

# write out the header: 
def writeHeader(config, outfile): 
  outfile.write("""<?xml version="1.0" encoding="utf-8"?>\n""")
  outfile.write("""<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:itunesu="http://www.itunesu.com/feed" version="2.0">\n""")
  outfile.write("  <channel>\n""")
  outfile.write("    <link>%s</link>\n" % (config.get('podcast', 'link')))
  outfile.write("    <language>%s</language>\n" % (config.get('podcast', 'language')))
  outfile.write("    <copyright>%s</copyright>\n" % (config.get('podcast', 'copyright')))
  outfile.write("    <webMaster>%s</webMaster>\n" % (config.get('podcast', 'webMaster')))
  outfile.write("    <managingEditor>%s</managingEditor>\n" % (config.get('podcast', 'managingEditor')))
  if config.get('podcast', 'hasImage') == "yes": 
    outfile.write("    <image>\n")
    outfile.write("      <url>%s</url>\n" % (config.get('podcast', 'imageURL')))
    outfile.write("      <title>%s</title>\n" % (config.get('podcast', 'imageTitle')))
    outfile.write("      <link>%s</link>\n" % (config.get('podcast', 'imageLink')))
    outfile.write("    </image>\n") 
  outfile.write("    <itunes:owner>\n")
  outfile.write("      <itunes:name>%s</itunes:name>\n" % (config.get('podcast', 'ownerName')))
  outfile.write("      <itunes:email>%s</itunes:email>\n" % (config.get('podcast', 'ownerEmail')))
  outfile.write("    </itunes:owner>\n") 
  outfile.write("""    <itunes:category text="%s">\n""" % (config.get('podcast', 'category')))
  outfile.write("""      <itunes:category text="%s" />\n""" % (config.get('podcast', 'subCategory')))
  outfile.write("    </itunes:category>\n")
  outfile.write("    <itunes:keywords>%s</itunes:keywords>\n" % (config.get('podcast', 'keywords')))
  outfile.write("    <itunes:explicit>%s</itunes:explicit>\n" % (config.get('podcast', 'explicit')))
  if config.get('podcast', 'hasImage') == "yes": 
    outfile.write("""    <itunes:image href="%s" />\n""" % (config.get('podcast', 'itunesImage')))
  outfile.write("""    <atom:link href="%s" rel="self" type="application/rss+xml" />\n""" % (config.get('podcast', 'feedURL')))
  timeNow=datetime.now().strftime("%a, %d %b %Y %H:%M:%S EST")
  outfile.write("    <pubDate>%s</pubDate>\n" % (timeNow))
  outfile.write("    <title>%s</title>\n" % (config.get('podcast', 'title')))
  outfile.write("    <itunes:author>%s</itunes:author>\n" % (config.get('podcast', 'author')))
  outfile.write("    <description>%s</description>\n" % (config.get('podcast', 'description')))
  outfile.write("    <itunes:summary>%s</itunes:summary>\n" % (config.get('podcast', 'description')))
  outfile.write("    <itunes:subtitle>%s</itunes:subtitle>\n" % (config.get('podcast', 'shortDescription')))
  outfile.write("    <lastBuildDate>%s</lastBuildDate>\n" % (timeNow))


#This expects a dictionary that will be described at a later date. 
# Dictionary: 
# id :: a unique ID for the episode 
# title :: title of the episode 
# link :: URL to the episode
# pubdate :: date of publication for the episode 
# creator :: creator field 
# series :: what series the episode is in. (Not used yet.) 
def addEpisode(info, outfile): 
  outfile.write("    <item>\n") 
  outfile.write("      <title>%s</title>\n" % (info['title']))
  outfile.write("      <pubDate>%s</pubDate>\n" % (info['pubdate']))
  outfile.write("      <itunes:order>%s</itunes:order>\n" % (info['id']))
  outfile.write("      <description>%s</description>\n" % (info['description']))
  outfile.write("      <itunes:summary>%s</itunes:summary>\n" % (info['description']))
  outfile.write("      <itunes:subtitle>%s</itunes:subtitle>\n" % (info['description']))
  length=info['length']
  outfile.write("""      <enclosure url="%s" type="audio/mpeg" length="%s" />\n""" % (info['link'], length))
  outfile.write("      <guid>%s</guid>\n" % (info['link']))
  duration="%1d:%02d:%02d" % (length/3600, (length/60)%60, length%60)
  outfile.write("      <itunes:duration>%s</itunes:duration>\n" % (duration))
  outfile.write("    </item>\n") 

def writeFooter(outfile): 
  outfile.write("  </channel>\n")
  outfile.write("</rss>\n")

if __name__ == "__main__": 
  
  config = configparser.ConfigParser() 
  config.read(sys.argv[1])
  try: 
    os.remove(config.get('podcast', 'outputFileName'))
  except OSError: 
    pass
  outfile = open(config.get('podcast', 'outputFileName'), 'w') 
  
  writeHeader(config, outfile)
  
  con = mdb.connect(config.get('database', 'host'), 
                    config.get('database', 'user'),
                    config.get('database', 'password'), 
                    config.get('database', 'database'))
  
  with con: 
    cur = con.cursor(mdb.cursors.DictCursor)
    
    database = config.get('database', 'table')

    cur.execute("SELECT * FROM " + database + " ORDER BY id DESC")
    
    episodes = cur.fetchall() 
    
    for episode in episodes: 
      addEpisode(episode, outfile) 
                    
  
    writeFooter(outfile) 
