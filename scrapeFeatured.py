#!/usr/bin/env python3 
"""Takes a CSV file as input and looks for new files in the database to add. 
Then if there's any new files to add, it will add them to the database.

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

import csv
import addEpisode
import sys
import urllib.parse

URL_PREFIX = "http://archive.spepmedia.com"

filemap = {"music": "music.ini", "sermon": "sermons.ini"}
writermap = dict() 
for key, value in filemap.items(): 
  writermap[key] = addEpisode.EpisodeWriter(value) 

def parseAndAdd(csvfile):
  with open(csvfile) as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
      if row[4] in filemap: 
        print(checkExistence(URL_PREFIX + urllib.parse.quote(row[1]), row[4]))
        print(', '.join(row))

def checkExistence(url, contentType):
  print(contentType)
  return writermap[contentType].checkExistence(url)
  
      
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage {} /path/to/featured.csv".format(sys.argv[0]))
    sys.exit(1)
  parseAndAdd(sys.argv[1])
  
  
