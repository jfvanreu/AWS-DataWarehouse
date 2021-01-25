"""
Includes all the queries used by our application
"""
import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

"""
We look the key variables defined in cfg file
DWH_ROLE_ARN
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
"""
DWH_ROLE_ARN = config.get("IAM_ROLE", "ARN")
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")


# DROP TABLES
staging_events_table_drop = "DROP table IF EXISTS staging_events"
staging_songs_table_drop = "DROP table IF EXISTS staging_songs"
songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"

# CREATE TABLES
staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (
                                                                            artist varchar, 
                                                                            auth varchar,
                                                                            firstName varchar,
                                                                            gender varchar,
                                                                            itemInSession int,
                                                                            lastName varchar,
                                                                            length float,
                                                                            level varchar,
                                                                            location varchar,
                                                                            method varchar,
                                                                            page varchar,
                                                                            registration varchar,
                                                                            sessionId int,
                                                                            song varchar,
                                                                            status int,
                                                                            ts bigint,
                                                                            userAgent varchar,
                                                                            userId int);
""")

staging_songs_table_create = ("""CREATE TABLE staging_songs (
                                                                num_songs int,
                                                                artist_id text,
                                                                artist_name varchar(max),
                                                                artist_latitude numeric,
                                                                artist_longitude numeric,
                                                                artist_location text,
                                                                song_id text,
                                                                title text,
                                                                duration numeric,
                                                                year int
                                                                )
""")


time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time timestamptz PRIMARY KEY, 
                                                         hour varchar, 
                                                         day varchar, 
                                                         week varchar, 
                                                         month varchar, 
                                                         year varchar, 
                                                         weekday varchar);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY, 
                                                          first_name varchar, 
                                                          last_name varchar, 
                                                          gender varchar, 
                                                          level varchar);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, 
                                                              name varchar, 
                                                              location varchar, 
                                                              latitude numeric, 
                                                              longitude numeric);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY, 
                                                          title text, 
                                                          artist_id text, 
                                                          year int, 
                                                          duration numeric);
""")

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays (songplay_id int IDENTITY(0,1) PRIMARY KEY, 
                                                                   start_time timestamptz NOT NULL, 
                                                                   user_id int NOT NULL, 
                                                                   level varchar, 
                                                                   song_id varchar, 
                                                                   artist_id varchar, 
                                                                   session_id int, 
                                                                   location varchar, 
                                                                   user_agent varchar);
""")

# INSERT RECORDS

# STAGING TABLES
# In this case we'll feed data from S3 using COPY
staging_events_copy = ("""copy staging_events from {}
                          credentials 'aws_iam_role={}'
                          region 'us-west-2'
                          json {};

""").format(LOG_DATA, DWH_ROLE_ARN, LOG_JSONPATH)

staging_songs_copy = ("""COPY staging_songs from {}
                        credentials 'aws_iam_role={}'
                        region 'us-west-2'
                        json 'auto';
                        
""").format(SONG_DATA, DWH_ROLE_ARN)

# FINAL TABLES
                                                
user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                            SELECT DISTINCT userId, firstName, lastName, gender, level
                            FROM staging_events
                            WHERE page = 'NextSong' AND userId NOT IN (SELECT DISTINCT user_id FROM users);
""")

song_table_insert = ("""INSERT INTO songs (artist_id, duration, song_id, title, year)
                            SELECT artist_id, duration, song_id, title, year FROM staging_songs;""")


artist_table_insert = ("""INSERT INTO artists (artist_id, latitude, location, longitude, name) 
                            SELECT artist_id, artist_latitude, artist_location, artist_longitude, artist_name 
                            FROM staging_songs;""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, month, week, weekday, year)
                            SELECT  timestamp 'epoch' + se.ts/1000 * interval '1 second' as start_time,
                                    DATE_PART(hrs, start_time),
                                    DATE_PART(dayofyear, start_time),
                                    DATE_PART(mons, start_time),
                                    DATE_PART(w, start_time),
                                    DATE_PART(dow, start_time),
                                    DATE_PART(yrs, start_time)
                            FROM staging_events se;""")

songplay_table_insert = ("""INSERT INTO songplays (artist_id, level, location, session_id, song_id, start_time, user_agent, user_id)
                                SELECT artist_id, level, location, sessionid, song_id, timestamp 'epoch' + ts/1000 * interval '1 second', useragent, userid
                                FROM staging_events AS events
                                JOIN staging_songs AS songs
                                ON (events.artist = songs.artist_name)
                                AND (events.song = songs.title);""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
