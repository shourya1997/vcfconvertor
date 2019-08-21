import hashlib, os
from datetime import datetime
import vcfconvert
import query_and_write

def to_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
        hashed = hasher.hexdigest()
    return hashed

def hash_compare():
    directory = 'query_files/'

    if len(os.listdir(directory)) < 1:
        print("Empty folder")

    elif len(os.listdir(directory)) == 1:
        return True

    else:
        creation = dict() # dict key: date to creation, value:filename
         
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                date_creation = filename[:len(filename)-4].split('_') # spliting filname to get date of creation
                dc = datetime.strptime(date_creation[1], '%Y-%m-%d|%H:%M:%S') # converting to datetime
                creation.update({dc:filename})
            
        creation_sorted = sorted(creation.keys(), reverse = True) # DESC sorting, of file creation datetime
        latest_query_file = creation[creation_sorted[0]] # lastest/last file
        old_query_file = creation[creation_sorted[1]] # 2nd last file

        latest_query_file_path = directory + str(latest_query_file)
        old_query_file_path = directory + str(old_query_file)

        latest_query_hash = to_hash(latest_query_file_path)
        old_query_hash = to_hash(old_query_file_path)

        if latest_query_hash != old_query_hash:
            print("DB Updated")
            return True
    
    return False
