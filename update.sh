#!/bin/sh

# Copyright (C) 2015 Joshua Gordon
# Licensed under GPLv2.

# Change to whatever your working directory is. 
cd /home/josh/podcast/ 

# Change this to the URL of your featured.csv. 
./scrapeFeatured.py /data/spep/spepmedia.com/featured.csv
./makePodcast.py sermons.ini
./makePodcast.py music.ini
