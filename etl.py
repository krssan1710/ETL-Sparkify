import os
import glob
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime
from sql_queries import *


def process_song_file(cur, filepath):
    """
        This function processes the JSON content of a song file to extract 
        song and artist information and load them into the 'songs' and 'artists' 
        tables respectively.
        
        INPUTS:
        * cur - the cursor variable to the Postgres database
        * filepath - path of the file to be read and processed.
    """
    # open song file
    df = pd.read_json(filepath,lines=True)
    df = df.replace(np.nan,0)

    # insert song record
    song_data = (
                 df['song_id'].values[0],
                 df['title'].values[0],
                 df['artist_id'].values[0],
                 df['year'].values[0].item(),
                 df['duration'].values[0].item()
                )
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = (
                    df['artist_id'].values[0],
                    df['artist_name'].values[0],
                    df['artist_location'].values[0],
                    df['artist_latitude'].values[0].item(),
                    df['artist_longitude'].values[0].item()
                  )
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
        This function processes the JSON content of a log file to extract 
        time and user information and load them into the 'time' and 'users' 
        tables respectively.
        
        The function then queries 'songs' and 'artists' tables to gather respective
        IDs and load the log data into the 'songplays' table.
        
        INPUTS:
        * cur - the cursor variable to the Postgres database
        * filepath - path of the file to be read and processed.
    """
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.DataFrame([datetime.fromtimestamp(t/1000) for t in df['ts']],columns=['dates'])
    
    # insert time data records
    time_data = [
                (
                    int(datetime.timestamp(time)*1000),
                    time.hour,
                    time.day,
                    time.week,
                    time.month,
                    time.year,
                    time.weekday()
                  ) 
                for time in t['dates']
                ]
    column_labels = ('starttime',
                     'hour',
                     'day',
                     'week',
                     'month',
                     'year',
                     'weekday')
    time_df = pd.DataFrame(data=time_data,columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId',
                  'firstName',
                  'lastName',
                  'gender',
                  'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
        
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.length, row.artist))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
                         row.ts,
                         row.userId,
                         row.level,
                         songid,
                         artistid,
                         row.sessionId,
                         row.location,
                         row.userAgent
                        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
        This function gathers the the paths of all files present
        within the folder specified in filepath parameter.
        
        Based on the value provided in the parameter 'func', it either
        invokes either process_song_file or process_log_file function
        
        INPUTS:
        * cur - the cursor variable to the Postgres database
        * conn - the connection variable to the Postgres database
        * filepath - path of the file to be read and processed
        * func - name of the process fucntion that must be invoked after gathering file paths
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
        The function connects to the target database, and gets a cursor
        for that database. It also initiates the file path of the folder
        containing all song and log files. It invokes process_data
        function to process song and log files.
    """
    conn = psycopg2.connect("host=localhost dbname=sparkifydb user=dataengguser password=learn@89")
    cur = conn.cursor()
    
    #process song files
    process_data(cur, conn, filepath='D:\\git\\Sparkify-ETL-Repo\\data\\song_data\\', func=process_song_file)
        
    #process log files
    process_data(cur, conn, filepath='D:\\git\\Sparkify-ETL-Repo\\data\\log_data\\', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()