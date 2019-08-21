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
    creation = dict()

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            date_creation = filename[:len(filename)-4].split('_')
            dc = datetime.strptime(date_creation[1], '%Y-%m-%d|%H:%M:%S')
            creation.update({dc:filename})
        
    creation_sorted = sorted(creation.keys(), reverse = True)
    latest_query_file = creation[creation_sorted[0]]
    old_query_file = creation[creation_sorted[1]]

    latest_query_file_path = directory + str(latest_query_file)
    old_query_file_path = directory + str(old_query_file)

    latest_query_hash = to_hash(latest_query_file_path)
    old_query_hash = to_hash(old_query_file_path)

    if latest_query_hash != old_query_hash:
        print("DB Updated")
        return True
    
    return False


