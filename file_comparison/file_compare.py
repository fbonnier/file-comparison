# List of comparison methods to compare two files and retrieve closest ones

# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

import os

# Global array that stores all files to compare
list_of_files01 = []
list_of_files02 = []


def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

def get_files_from_watchdog_log (watchdog_file):
    list_of_files = []

    with open (watchdog_file, 'r') as f1:
        lines = f1.readlines()
        for irawline in lines :
            iline = irawline.split('\n')[0]
            src_dest = iline.split()
            for ifile in src_dest:
                if ifile not in list_of_files:
                    list_of_files.append(ifile)

    print (list_of_files)
    return list_of_files

def find_bijective (f1, f2):

    # Read files from watchdog logs
    list_of_files01 = get_files_from_watchdog_log (f1)
    print ("List of files 01")
    print (list_of_files01)
    list_of_files02 = get_files_from_watchdog_log (f2)
    print ("List of files 02")
    print (list_of_files02)

    # Score Matrix
    score_matrix = []

    # Loop over all files in list01 and list02 and compute a score for each write_code_location
    for ifile in list_of_files01:
        # Gives the first row
        irow = []
        for jfile in list_of_files02:
            try:
                irow.append (hash_from_file_info(ifile, jfile))
            except FileNotFoundError as e:
                print (e)
                irow.append(0.)
            score_matrix.append(irow)
    print ("Score Matrix ::")
    print (score_matrix)

    # Print best score per row
    for irow in score_matrix:
        score_max = 0.
        for ival in irow:
            if ival > score_max:
                score_max = ival

        print ("Score Max of this row = " + str (score_max))



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
    return (ratio*100)
    ## Hash is done using Nilsimsa algorithm to get strong colisions
    # f1_hash = Nilsimsa (bytes(os.path.dirname + ))
