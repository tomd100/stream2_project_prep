import re
from pymongo import MongoClient
import json
import csv

from auth import MONGODB_URI

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def get_stripped():
    
    album_list = [];
    song_list = [];
    stripped_list = [];
    #--------------------------------------------------------------------------- 
    # Upload stripped album list
    
    with open("text_files/album_stripped_list.txt", "r") as inFile:
        for line in inFile:
            line = line[:-1]    # remove end-of-line char
            album_list.append(line);
    inFile.close();
    
    #--------------------------------------------------------------------------- 
    # Download all songs from mongodb
    
    song_list = list(download_mongo("bob_dylan_songs"))
    for song in song_list:
        if song["album"] in album_list and song["num_plays"] != "0":
            
            stripped_list.append(song)

    return stripped_list
    
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def upload_mongo(song_list, collection_name):
    
    database_name = "stream2_project";
    collection_name= collection_name;
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];
        existing_collections = db.collection_names();

        if collection_name in existing_collections:
            collection.drop();
       
        collection.insert_many(song_list)

# ------------------------------------------------------------------------------
        
def download_mongo(collection_name):
    
    database_name = "stream2_project";
    
    fields = {'song_title': True, 'song_chart_pos': True, 'album': True, 'album_year': True, 
        'first_date': True, 'last_date': True, 'num_plays': True, '_id': False}
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];
        song_list = collection.find(projection=fields)
        song_list = list(song_list);
        
    return song_list

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

stripped_list = get_stripped()
upload_mongo(stripped_list, "stripped_song_list")





                        
                    
