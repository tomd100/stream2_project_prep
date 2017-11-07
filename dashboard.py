from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

# from auth import MONGODB_URI

app = Flask(__name__)

mongodb_uri = os.environ.get('mongodb_uri')
dbs_name = os.environ.get('mongo_db_name','stream2_project')
collection_name = os.environ.get('mongo_collection_name','bob_dylan_songs')

fields = {'song_title': True, 'song_chart_pos': True, 'album': True, 'album_year': True, 'first_date': True, 'last_date': True, 'num_plays': True, '_id': False}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bob_dylan_songs")
def get_bob_dylan_songs():
    with MongoClient(mongodb_uri) as conn:
        collection = conn[dbs_name][collection_name]
        bob_dylan_songs = collection.find(projection=fields)
        return json.dumps(list(bob_dylan_songs))

@app.route("/top_30_songs")
def get_top_30_songs():
    with MongoClient(mongodb_uri) as conn:
        collection = conn[dbs_name][collection_name]
        top_30_songs = collection.find(projection=fields)
        return json.dumps(list(top_30_songs))


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('port', 8080)))

