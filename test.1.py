
from pymongo import MongoClient
import json
import os

from auth import MONGODB_URI

mongo_db_name = "stream2_project"
collection_name = "bob_dylan_songs"

fields = {'song_title': True, 'song_chart_pos': True, 'album': True, 'album_year': True, 'first_date': True, 'last_date': True, 'num_plays': True, '_id': False}

with MongoClient(MONGODB_URI) as conn:
    db = conn[mongo_db_name];
    collection = db[collection_name];
    song_list = collection.find(projection=fields);

song_list = list(song_list);
for song in song_list:
    if song["album_year"] == "2012":
        fd = song["first_date"];
        ld = song["last_date"];
        
        fd.parse("%d/%m/%Y")
        # date_diff = ld.getTime() - fd.getTime();
        
        print(song["album"], song["num_plays"], song["first_date"], song["last_date"], song["album_year"])
