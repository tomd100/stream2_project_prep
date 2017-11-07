from pymongo import MongoClient
import json
import os

from auth import MONGODB_URI

path = "json_files/"

def download_json(collection_name, file_name):
    mongo_db_name = "stream2_project"
    
    file_name = path + file_name;
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

# download_json("bob_dylan_songs", "output.json");    
# download_json("bob_dylan_songs", "bob_dylan_songs.json");
# download_json("top_30_songs", "top_30_songs.json");
