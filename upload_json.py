from pymongo import MongoClient
import re
import json
import os

from auth import MONGODB_URI

path = "json_files/"

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def upload_mongo(file_name, collection_name):
    
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






                        
                    
