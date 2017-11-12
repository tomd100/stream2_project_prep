import re
from pymongo import MongoClient
import json
import csv

import sys
sys.path.insert(0, '../../mongodb_auth')

from auth import MONGODB_URI

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def parse_text():
    
    album_list = [];
    
    album_ry_dict = {};
    album_ry_list = [];
    
    song_chart_dict = {};
    song_chart_list = [];

    song_list = [];
    
    #--------------------------------------------------------------------------- 
    
    # Album list
    file_name = path_to_data + "album_list.txt"
    with open(file_name, "r") as inFile:
        for line in inFile:
            line = line[:-1]    # remove end-of-line char
            album_list.append(line);
    inFile.close();
    
    # Album release year
    file_name = path_to_data + "album_release_years.txt"
    with open(file_name, "r") as inFile:
        for line in inFile:
            line = line[:-1]    # remove end-of-line char
            pos = line.find("(");
            album_name = line[:pos];
            album_name = album_name.strip();
            album_ry_dict["album"] = album_name;
            
            album_year = line[pos:]
            album_year = album_year[1:5]
            album_ry_dict["year"] = album_year;
            
            album_ry_list.append(album_ry_dict.copy());
            
    inFile.close();
    
    # Song chart position
    file_name = path_to_data + "top_30_tracks.csv"
    with open(file_name, newline ='') as inFile:
        for line in inFile:
            line = line.split(",",1);
            song_chart_dict["pos"] = line[0].strip();
            song_chart_dict["song"]  = line[1].strip();
            
            song_chart_list.append(song_chart_dict.copy());            
    inFile.close();

    #---------------------------------------------------------------------------     
    file_name = path_to_data + "bd_web_page_copy.txt"
    with open(file_name, 'r') as inFile:
        
        for line in inFile:
            
            line = line[:-1]; # remove end-of-line char.            

            song = {};
            
            song_title = "";
            album = "";
            dates = "";
            first_date = "";
            last_date = "";
            num_plays = 0;
            
        #----------------------------------------------------------------------- 
            # Find dates
            
            # Find first and second date, if they exist
            pos = find_dates(line);
            
            if pos == 0:
                dates = ""
                first_date = "";
                last_date = "";
            else:
                dates = line[pos:pos + 26]; 
                dates = dates.strip();                
                line = line.replace(dates, " ");
                
                dates = dates.split(" ");
                dates = " ".join(dates[:3]), " ".join(dates[3:]);
                first_date = fix_date(dates[0]);
                last_date = fix_date(dates[1]);
                
            # Line is now without the date fields
        #----------------------------------------------------------------------- 
            # find number of plays   
            
            num_plays = get_num_plays(line);
            line = line[:-len(num_plays)];
            line = line.strip();
            
            # line is left with just album (if it exists) and song title
        #----------------------------------------------------------------------- 
            # Search for album and remove if exists
            album = get_album(line, album_list);
            if album == "":
                song_title = line;
            else:
                song_title = line[:-len(album)];

        #----------------------------------------------------------------------- 
            # Search for album release year 
            if album == "":
                album_year = "";
            else:
                album_year = get_album_release_year(album, album_ry_list);

        #----------------------------------------------------------------------- 
            # Search for song ranking 
            song_chart_pos = get_song_chart_pos(song_title, song_chart_list);
            
        #----------------------------------------------------------------------- 
            
            # print("song: {0}".format(song_title));
            # print("song_chart_pos: {0}".format(song_chart_pos));
            # print("album: {0}".format(album));
            # print("album_year: {0}".format(album_year));
            # print("first date: {0}".format(first_date));
            # print("last date: {0}".format(last_date));
            # print("num plays: {0}".format(num_plays));
            # print("\n")
    
            song['song_title'] = song_title;
            song['song_chart_pos'] = song_chart_pos;
            song['album'] = album;
            song['album_year'] = album_year;
            song["first_date"] = first_date;
            song["last_date"] = last_date;
            song["num_plays"] = num_plays
                
            song_list.append(song);
    
    file_name = path_to_json + "output.json"
    outFile = open(file_name, "+w")    
    outFile.write(json.dumps(song_list));
    outFile.close()
    
    inFile.close()
    return song_list
    
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def find_dates(line):
    p1 = -1;
    p2 = -1
    pos = -1;
    date_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    
    rev_line = line[::-1];
    
    for date in date_list:
        date = " " + date + " ";
        rev_date = date[::-1];
        pos = rev_line.find(rev_date);
        if pos > -1:
            if p1 > pos or p1 == -1:
                p1 = pos; 

    if p1 > -1:
        for date in date_list:
            date = " " + date + " ";
            rev_date = date[::-1];
            pos = rev_line[p1 + 1:].find(rev_date);
            if pos > -1:
                if p2 > pos or p2 == -1:
                    p2 = pos;
    if p2 == 12:
        return len(line) - (p1 + 17);
    else:
        return 0;

# ------------------------------------------------------------------------------

def fix_date(date):
    date_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    
    date = date.split(" ");
    
    month_text = date[0];    
    month = date_list.index(month_text) + 1; 
    if month < 10:
        month = "0" + str(month);
    else:
        month = str(month);
    
    day = date[1];
    day = day.split(",");
    day = day[0]
    
    year = date[2]
    
    new_date = day + "/" + month + "/" + year;

    return new_date;

# ------------------------------------------------------------------------------

def get_num_plays(line):
    
    pos = -1;
    num_plays = "";
    first_part = "";
    
    rev_line = line[::-1];
    first_char = rev_line[0];
    
    pos = rev_line.find(" ");
    if pos > -1:
        first_part = rev_line[:pos];
        first_part = first_part.strip();
        if first_part.isdigit() and len(first_part) <= 4:
            num_plays = first_part[::-1];
        else:
            num_plays = "0";
    else: 
        num_plays = "0";

    return num_plays;

# ------------------------------------------------------------------------------

def get_album(line, album_list):
    
    pos = -1;
    album_found = "";
    len_album = 0;
    
    rev_line = line[::-1];

    for album in album_list:
        rev_album = album[::-1];
        pos = rev_line.find(rev_album);
        if pos == 0:                    # Album name must start at the beginning of rev_line
            if len(album) > len_album:  # Some album names are also within larger album names
                len_album = len(album);
                album_found = album;
                
    return album_found;

# ------------------------------------------------------------------------------

def get_album_release_year(album, album_ry_list):
    
    album_year = ""
    
    for album_ry in album_ry_list:
        if album_ry["album"].lower() == album.lower():
            album_year = album_ry["year"];
    
    return album_year;
    
# ------------------------------------------------------------------------------

def get_song_chart_pos(song_title, song_chart_list):
    
    song_chart_pos = "-1";
    
    for song_chart in song_chart_list:
        if song_chart["song"].lower() == song_title.lower():
            song_chart_pos = song_chart["pos"];
            
    return song_chart_pos;

# ------------------------------------------------------------------------------

def upload_mongo(song_list, collection_name):
    
    database_name = "stream2_project";
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];
        existing_collections = db.collection_names();

        if collection_name in existing_collections:
            collection.drop();
       
        outFile = open("output.json", "+w")    
        outFile.write(json.dumps(song_list));
        outFile.close()
         
        collection.insert_many(song_list)

# ------------------------------------------------------------------------------
        
def download_mongo(collection_name):
    
    database_name = "stream2_project";

    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];

        song_list = list(collection.find({}));
        
    return song_list

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def verify_data(song_list):
    
    album_set = set();
    song_set = set();
    id_set = set();
    
    for song in song_list:
        album_set.add(song["album"]);
        song_set.add(song["song_title"]);
        id_set.add(song["_id"]);
    
    print("Total records: {0}".format(len(song_list)));    
    print("Total unique albums: {0}".format(len(album_set)));    
    print("Total unique songs: {0}".format(len(song_set)));    
    print("Total unique ids (mongo): {0}".format(len(id_set)));  
    print("\n")
    
    file_name = path_to_text + "song_list.txt"
    outFile = open(file_name, "+w")    
    song_list_sorted = list(song_set);
    song_list_sorted.sort()
    
    for x, song in enumerate(song_list_sorted):
        outFile.write(song);
        if x < len(song_list_sorted) - 1:
            outFile.write("\n");
    outFile.close()
    
    # Verify that all songs in top-30 are in overall song list
    
    song_list_import = [];
    top_30_list = [];
    
    file_name = path_to_text + "song_list.txt"
    with open(file_name, "r") as songFile:
        for line in songFile:
            song_list_import.append(line.strip());
    songFile.close();
    
    file_name = path_to_data + "top_30_tracks.csv"
    with open(file_name, "r") as topFile:
        for line in topFile:
            line = line.split(",",1)
            top_30_list.append(line[1].strip());
    topFile.close();
    
    for song in top_30_list:
        if song not in song_list_import:
            print(song)
    return

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

path_to_data = "../data/";
path_to_text = "../../text_files/";
path_to_json = "../../json_files/";

song_list = parse_text();     
# upload_mongo(song_list, "bob_dylan_songs");

song_list = download_mongo("bob_dylan_songs");
verify_data(song_list);




                        
                    
