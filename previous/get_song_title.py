import re
from flask import Flask, request, render_template
from pymongo import MongoClient
import os
import tweepy
import json

from auth import MONGODB_URI


def parse_text():
    
    song_list = []
    
    
    i = 0
    
    with open("bd_web_page_copy.txt", 'r') as infile:
        
        upper = "[A-Z]"
        lower = "[a-z]"
        number = "[0-9]"
        
        for line in infile:
            
            song = {}
            
            song_title = "";
            album = "";
            dates = "";
            first_date = "";
            last_date = "";
            num_plays = "";

            full_line = line;
            x = 0
            while x < len(line):
                if (re.search(lower,line[x]) or line[x] == ")") and (re.search(upper,line[x+1]) or line[x + 1] == '”'):
                    song_title = line[:x + 1];
                    line = line[x + 1:];
                x += 1  
                
            rev_line = line[::-1]; 
            rev_line = rev_line[1:] 
            
            if rev_line[0] == "0" and re.search(number,rev_line[1]) is not "none":
                num_plays = 0;
                dates = "";
                rev_line = rev_line[1:];
                album = rev_line[::-1];
            else:
                num_plays = int(rev_line.split(" ",1)[0]);
                rev_line = rev_line.split(" ", 1)[1];
                dates = rev_line[:25];
                rev_line = rev_line[25:];
                line = rev_line[::-1];
                
                dates = dates[::-1];
                dates = dates.split(" ");
                dates = " ".join(dates[:3]), " ".join(dates[3:]);
                first_date = dates[0];
                last_date = dates[1];
                
                album = line;
                
            song['song_title'] = song_title;
            song['album'] = album;
            song["first_date"] = first_date;
            song["last_date"] = last_date;
            song["num_plays"] = num_plays
                
            song_list.append(song);

            # print("song: {0}".format(song_title, album, dates, num_plays))
            # print("album: {1}".format(song_title, album, dates, num_plays))
            # print("dates: {2}".format(song_title, album, dates, num_plays))
            # print("num plays: {3}".format(song_title, album, dates, num_plays))
            
            # outFile.write(song_title + ",");
            # outFile.write(album + ",");
            # outFile.write(first_date + ",");
            # outFile.write(last_date + ",");
            # outFile.write(str(num_plays)); 
            # outFile.write("\n");
    
    # outFile = open("output.json", "+w")    
    # outFile.write(json.dumps(song_list));
    # outFile.close()
    
    # print (song_list)
    
    infile.close()
    return song_list



def load_mongo(song_list):
    
    database_name = "stream2_project";
    collection_name= "bob_dylan_songs";
    
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
        
        
song_list = parse_text()     
# print(song_list)
load_mongo(song_list)
                        
                    
