from pymongo import MongoClient
import re
import json
import os

import sys
sys.path.insert(0, '../mongodb_auth')

from auth import MONGODB_URI

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def download_json(collection_name, file_name):
    mongo_db_name = "stream2_project"
    
    file_name = path_to_json + file_name;
    print(file_name)
        
    fields = {'song_title': True, 'song_chart_pos': True, 'album': True, 'album_year': True, 'first_date': True, 'last_date': True, 'num_plays': True, '_id': False}
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[mongo_db_name];
        collection = db[collection_name];
        song_list = collection.find(projection=fields);
    
    song_list = list(song_list);
        
    outFile = open(file_name, "+w");
    outFile.write(json.dumps(song_list));
    outFile.close();
    return;

# ------------------------------------------------------------------------------

def upload_json(collection_name, file_name):
    mongo_db_name = "stream2_project"
    
    file_name = path_to_json + file_name;
        
    with open(file_name) as inFile:    
        song_list = json.load(inFile)

    song_list = list(song_list);
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[mongo_db_name];
        collection = db[collection_name];
        collection.insert_many(song_list);
    
    return;

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
    
path_to_json = "../json_files/"

# download_json("bob_dylan_songs", "output.json");    
# download_json("bob_dylan_songs", "bob_dylan_songs.json");
# download_json("top_30_songs", "top_30_songs.json");
# download_json("stripped_song_list", "stripped_songs.json");

upload_json("test", "stripped_songs.json");
