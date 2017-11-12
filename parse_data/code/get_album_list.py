import re
import json

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def parse_for_albums():
    
    album_set = set();
    album_list = [];
    
    file_name = path_to_data + "bd_web_page_copy.txt"
    with open(file_name, 'r') as inFile:
        
        upper = "[A-Z]"
        lower = "[a-z]"
        number = "[0-9]"
        
        for line in inFile:
            
            line = line[:-1];       # remove end-of-line char.
            
            album = "";
            
            rev_line = line[::-1];  # reverse line
            
            if rev_line[0] == "0" and (re.search(number,rev_line[1]) is None or rev_line.find(" ") > 3):
                rev_line = rev_line[1:];
            else:
                rev_line = rev_line.split(" ", 1)[1];
                rev_line = rev_line[25:];
            
            line = rev_line[::-1];    
            # print(line)
            
            album_pos = 0;
            x = 0;
            while x < len(line) - 1:
                if line[x] == "M" and line[x + 1] == "c":
                    x += 1; # move passed "Mc"
                elif re.search(lower,line[x]) and re.search(upper,line[x+1]):
                    album_pos = x + 1
                    album_name = line[album_pos:];
                    album_name = album_name.strip();
                    # if album_name == "Another Side Of Bob Dylan Jul 04, 1978 Jul 08, 2012 26":
                    #     print(line);
                    album_set.add(album_name);
                x += 1
            
    inFile.close()
    #  additional albums to add to list. 
    album_set.add('“Love And Theft”');
    
    # convert to list in order to sort
    album_list = list(album_set);
    album_list.sort()
    
    # output album list to file.
    file_name = path_to_data + "album_list.txt"
    
    outFile = open(file_name, "+w")
    for x, album in enumerate(album_list):
        outFile.write(album);
        if x < len(album_list) - 1:
            outFile.write("\n");
    outFile.close();    
    
    return;

# ------------------------------------------------------------------------------    

def check_for_other_albums():
    
    album_list = [];
    
    file_name = path_to_data + "album_list.txt";
    with open(file_name, "r") as albumFile:
        for line in albumFile:
            line = line[:-1]
            album_list.append(line);
    albumFile.close();
        
    outFile = open(path_to_data + "missing_albums.txt", "+w");
    
    with open(path_to_data + "bd_web_page_copy.txt", 'r') as inFile:
        for line in inFile:
            pos = -1;
            found = 0;
            for album in album_list:
                pos = line.find(album);
                if pos > -1:
                    found = 1;
            if found == 0:
                outFile.write(line);
        
    outFile.close();
    return;

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

path_to_data = "../data/";
path_to_text = "../../text_files/";
path_to_json = "../../json_files/";


parse_for_albums()     
check_for_other_albums()  
print("check complete")
    


