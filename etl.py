import psycopg2
import os
import glob
import pandas as pd
from Project_Sql_Queries import *

def song_process(cur, path):
    df = pd.read_json(path, lines=True)
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    cur.execute(insert_song_table, song_data)
    
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    cur.execute(insert_artist_table, artist_data)
    
def log_data_process(cur, path):
    df = pd.read_json(path, lines=True)
    df = df[df['page'] == 'NextSong']
    
    t = pd.to_datetime(df['ts'])
    
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_datas = [(time.value, time.hour, time.day, time.week, time.month, time.year, time.weekday()) for time in t]
    time_df = pd.DataFrame(data=time_datas, columns=column_labels)
    
    for i, row in time_df.iterrows():
        cur.execute(insert_time_table, list(row))
    
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    for i, row in user_df.iterrows():
        cur.execute(insert_user_table, list(row))
        
    for i, row in df.iterrows():
        cur.execute(select_song, (row.song, row.artist, row.length))
        result = cur.fetchone()
        if result:
            songid, artistid = result
        else:
            songid, artistid = None, None
        songplay_data = (i, row['ts'], row['userId'], row['level'], songid, artistid, row['sessionId'],
                        row['location'], row['userAgent'])
        cur.execute(insert_songplays_table, songplay_data)

def data_process(cur, conn, path, func):
    all_files = []
    for root, dirs, files in os.walk(path):
        files = glob.glob(os.path.join(root, '*.json'))
        for file in files:
            all_files.append(os.path.abspath(file))
    
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, path))
    
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

def main():
    conn = psycopg2.connect('host=localhost dbname=songstarschema user=postgres password=root port=5432')
    cur = conn.cursor()

    data_process(cur, conn, path='data/song_data', func=song_process)
    data_process(cur, conn, path='data/log_data', func=log_data_process)

    conn.close()
    
if __name__ == '__main__':
    main()