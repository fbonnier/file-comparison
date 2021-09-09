# List of comparison methods to compare two files and retrieve closest ones

# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

import os

# Global array that stores all files to compare
list_of_files = []


def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

def get_files_from_watchdog_log (watchdog_file):
    global list_of_files
    
    with open (watchdog_file, 'r') as f1:
        lines = f1.readlines()
        for iline in lines :
            if iline not in list_of_files:
                list_of_files.append(iline)
                
    print (list_of_files)
    return 

def hash_from_file_info (f1_path, f2_path):
    ## Hash file informations
    #   * file name
    #   * file size
    #   * file path
    print ("Dirname = " + os.path.dirname(f1_path))
    print ("Basename = " + os.path.basename(f1_path))
    print ("Size = " + str(os.path.getsize(f1_path)))
    all_info_f1 = os.path.basename(f1_path) + str(os.path.getsize(f1_path))
    all_info_f2 = os.path.basename(f2_path) + str(os.path.getsize(f2_path))
    print (all_info_f1)
    print (Nilsimsa(all_info_f1))
    print (all_info_f2)
    print (Nilsimsa(all_info_f2))
    ratio = compute_ratio (compare_digests (Nilsimsa(all_info_f1).hexdigest(), Nilsimsa(all_info_f2).hexdigest()))
    print ("FINFO Ratio = " + str(ratio*100))
    ## Hash is done using Nilsimsa algorithm to get strong colisions
    # f1_hash = Nilsimsa (bytes(os.path.dirname + ))
