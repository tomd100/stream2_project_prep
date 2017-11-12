import re
import sqlite3
import json
from pymongo import MongoClient

import sys
sys.path.append('../mongodb_auth')
sys.path.append('../utils')

from auth import MONGODB_URI
from mongodb_list import download_mongo

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def db_connect(path, database):
    
    # connect to database
    conn = sqlite3.connect(path + database)
    return conn;

# ------------------------------------------------------------------------------

def db_create_tables(conn):
    c = conn.cursor();

    # albums
    sql = "SELECT COUNT(*) FROM SQLITE_MASTER WHERE TYPE='table' AND NAME='albums'"
    c.execute(sql)
    num_rows = c.fetchone()

    if num_rows[0] == 1:
        sql = "DROP TABLE albums";
        c.execute(sql);

    sql = "CREATE TABLE albums (id int, album text, album_year text)"
    c.execute(sql)

    #songs
    sql = "SELECT COUNT(*) FROM SQLITE_MASTER WHERE TYPE='table' AND NAME='songs'"
    c.execute(sql)
    num_rows = c.fetchone()

    if num_rows[0] == 1:
        sql = "DROP TABLE songs";
        c.execute(sql);

    sql = "CREATE TABLE songs (id int, song_title text)"
    c.execute(sql)
    
    conn.commit()
    return

# ------------------------------------------------------------------------------

def db_insert_data(conn, song_list):
    c = conn.cursor();
    
    album_set = set();
    album_list = [];

    song_title_set = set();
    song_title_list = [];
    
    i = 0;
    j = 0;
    
    for song in song_list:
        if song["album"] not in album_set:
            album_set.add(song["album"]);
            i += 1
            album_list.append({"id": str(i), "album": song["album"]})
            song["album_id"] = i;
            sql = "INSERT INTO albums VALUES( {}, '{}', '{}')".format(i, song["album"], song["album_year"])
            
            c.execute(sql);
            conn.commit()
        else:
            album_list_item = next((item for item in album_list if item["album"] == song["album"]))
            song["album_id"] = album_list_item["id"]
    

        if song["song_title"] not in song_title_set:
            song_title_set.add(song["song_title"]);
            j += 1
            song_title_list.append({"id": str(j), "song_title": song["song_title"]})
            song["song_id"] = j;
            sql = "INSERT INTO songs VALUES( {}, '{}')".format(j, song["song_title"])
            
            c.execute(sql);
            conn.commit()
        else:
            song_title_list_item = next((item for item in song_title_list if item["song_title"] == song["song_title"]))
            song["song_id"] = song_title_list_item["id"]
    
    return
# ------------------------------------------------------------------------------

def db_select(data, table_name):
    sql = "SELECT " + data + " FROM " + table_name;
    return sql;
    

# ------------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def main():
    
    path = "../verify_data/sqlite3/"
    database = "songs.db"
    
    conn = db_connect(path, database)
    
    song_list = download_mongo("bob_dylan_songs");
    
    db_create_tables(conn);
    db_insert_data(conn, song_list);
    
      
  
    # for song in song_list:
    #     print(song["song_id"], song["song_title"])
        
    # for song in song_title_list :
    #     print(song)
    
    # create album table
    # db_ct_album(conn);
    # db_insert(conn,  )
    # db_select("*", "album", )
    
    

    
    
    conn.close()
    return

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
    