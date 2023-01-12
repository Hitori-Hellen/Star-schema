dim_time = ("""
CREATE TABLE time 
    (start_time bigint PRIMARY KEY,
    hour int,
    day int,
    week int,
    month int,
    year int,
    weekday int);
""")

dim_user = ("""
CREATE TABLE users 
    (user_id int PRIMARY KEY,
    first_name varchar,
    last_name varchar,
    gender varchar,
    level varchar);            
""")

dim_song = ("""
CREATE TABLE songs
    (song_id varchar PRIMARY KEY,
    title varchar,
    artist_id varchar,
    year int,
    duration float);
""")

dim_artist = ("""
CREATE TABLE artists
    (artist_id varchar PRIMARY KEY,
    name varchar,
    location varchar,
    latitude float,
    longitude float);              
""")

fact_songplay = ("""
CREATE TABLE songplays
    (songplay_id int PRIMARY KEY,
    start_time bigint REFERENCES time(start_time) ON DELETE RESTRICT,
    user_id int REFERENCES users(user_id) ON DELETE RESTRICT,
    song_id varchar REFERENCES songs(song_id) ON DELETE RESTRICT,
    artist_id varchar REFERENCES artists(artist_id) ON DELETE RESTRICT,
    level varchar,
    session_id int,
    location varchar,
    user_agent varchar);
""")

drop_songplay = "DROP TABLE IF EXISTS songplays"
drop_time = "DROP TABLE IF EXISTS time"
drop_user = "DROP TABLE IF EXISTS users"
drop_song = "DROP TABLE IF EXISTS songs"
drop_artist = "DROP TABLE IF EXISTS artists"

insert_song_table = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT(song_id)
DO NOTHING;
""")

insert_artist_table = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT(artist_id)
DO NOTHING;
""")

insert_time_table = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT(start_time)
DO NOTHING;
""")

insert_user_table = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE 
SET level=excluded.level;
""")

select_song = ("""
SELECT songs.song_id, artists.artist_id FROM songs
JOIN artists ON songs.artist_id=artists.artist_id
WHERE songs.title=%s AND artists.name=%s AND songs.duration=%s; 
""")

insert_songplays_table = ("""
INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, 
                       session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (songplay_id) 
DO NOTHING;
""")

create_table_sql = [dim_time, dim_song, dim_artist, dim_user, fact_songplay]
drop_table_sql = [drop_songplay, drop_song, drop_artist, drop_time, drop_user]