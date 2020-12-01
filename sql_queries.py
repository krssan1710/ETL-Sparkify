# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS  songs;"
artist_table_drop = "DROP TABLE IF EXISTS  artists;"
time_table_drop = "DROP TABLE IF EXISTS  time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
songplay_id SERIAL CONSTRAINT songplays_pk PRIMARY KEY,
starttime BIGINT REFERENCES time (starttime),
user_id BIGINT REFERENCES users (user_id),
level TEXT,
song_id TEXT REFERENCES songs (song_id),
artist_id TEXT REFERENCES artists (artist_id),
session_id BIGINT,
location TEXT,
user_agent TEXT
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
user_id BIGINT CONSTRAINT users_pk PRIMARY KEY,
first_name TEXT,
last_name TEXT,
gender char,
level TEXT
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
song_id TEXT  CONSTRAINT songs_pk PRIMARY KEY,
title TEXT,
artist_id TEXT,
year INT,
duration FLOAT
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
artist_id TEXT CONSTRAINT artists_pk  PRIMARY KEY,
name TEXT,
location TEXT,
latitude INT,
longitude INT
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
starttime BIGINT CONSTRAINT time_pk  PRIMARY KEY,
hour INT,
day INT,
week INT,
month INT,
year INT,
weekday INT
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (
starttime,
user_id,
level,
song_id,
artist_id,
session_id,
location,
user_agent
) 
VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
""")

user_table_insert = ("""
INSERT INTO users (
user_id,
first_name,
last_name,
gender,
level
) 
VALUES (%s,%s,%s,%s,%s) 
ON CONFLICT(user_id) DO UPDATE SET 
first_name=EXCLUDED.first_name,
last_name=EXCLUDED.last_name,
gender=EXCLUDED.gender,
level=EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (
song_id,
title,
artist_id,
year,
duration
) 
VALUES (%s,%s,%s,%s,%s) 
ON CONFLICT(song_id) DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (
artist_id,
name,
location,
latitude,
longitude
) 
VALUES (%s,%s,%s,%s,%s) 
ON CONFLICT(artist_id) DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO time (
starttime,
hour,
day,
week,
month,
year,
weekday
) 
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING;
""")

# TRUNCATE TABLES
songplay_truncate = ("""TRUNCATE TABLE songplays;""")

# FIND SONGS

song_select = ("""
SELECT song_id,songs.artist_id 
FROM songs 
INNER JOIN artists 
ON songs.artist_id=artists.artist_id 
WHERE 
songs.title=%s AND songs.duration=%s 
AND artists.name=%s;
""")

# QUERY LISTS

create_table_queries = [artist_table_create, song_table_create, user_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]