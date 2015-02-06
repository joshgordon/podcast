# Podcast
This is a simple set of scripts that I wrote in python to make a podcast feed
with stuff stored in a mysql database. 

Your mysql table should look like this

```+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| id          | int(11)       | NO   | PRI | NULL    | auto_increment |
| title       | varchar(512)  | YES  |     | NULL    |                |
| link        | varchar(1024) | YES  |     | NULL    |                |
| pubdate     | varchar(255)  | YES  |     | NULL    |                |
| creator     | varchar(255)  | YES  |     | NULL    |                |
| series      | varchar(255)  | YES  |     | NULL    |                |
| description | varchar(1024) | YES  |     | NULL    |                |
| shortDesc   | varchar(255)  | YES  |     | NULL    |                |
| length      | int(11)       | YES  |     | NULL    |                |
| comment     | varchar(255)  | YES  |     | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+
```

These scripts support multiple podcasts by having multiple config files. Config
files are specified on the command line. 

this can be done with 

```
create table music(id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, title varchar(512), link varchar(1024), pubdate varchar(255), creator varchar(255), series varchar(255), description varchar(1024), shortDesc varchar(255), length int(11), comment varchar(255)); 
```

## Example
    ./makePodcast.py example.ini 

Add episode currently rips some metadata off of the mp3 file. It's currently 
formatted to fit my Church's needs, because that's the primary reason I wrote 
these scripts. It shouldn't be terribly difficult to extend it to whatever you 
need. This *ought* to be configurable in the future. 

    ./addEpisode.py example.ini http://example.com/episode.mp3
