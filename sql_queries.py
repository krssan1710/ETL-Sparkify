# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS  songs;"
artist_table_drop = "DROP TABLE IF EXISTS  artists;"
time_table_drop = "DROP TABLE IF EXISTS  time;"

# CREATE TABLES

songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplays(songplay_id bigint,starttime bigint,user_id bigint,level text,song_id bigint,artist_id bigint,session_id bigint,location text,user_agent text)")

user_table_create = ("CREATE TABLE IF NOT EXISTS users(user_id bigint,first_name text,last_name text,gender char,level text);")

song_table_create = ("CREATE TABLE IF NOT EXISTS songs(song_id bigint,title text,artist_id bigint,year int,duration int);")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artists(artist_id bigint,name text,location text,latitude int,longitude int);")

time_table_create = ("CREATE TABLE IF NOT EXISTS songplays(starttime bigint,hour int,day int,week int,month int,year int,weekday int);")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]