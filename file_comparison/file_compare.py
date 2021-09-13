# List of comparison methods to compare two files and retrieve closest ones

# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

import os

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
    list_of_files_rows = get_files_from_watchdog_log (f1)
    print ("List of files rows")
    print (list_of_files_rows)
    list_of_files_cols = get_files_from_watchdog_log (f2)
    print ("List of files cols")
    print (list_of_files_cols)

    # Score Matrix
    score_matrix = []

    # # Loop over all files in list01 and list02 and compute a score for each write_code_location
    for ifile in list_of_files_rows:
        # Gives the first row
        irow = []
        for jfile in list_of_files_cols:
            try:
                irow.append (hash_from_file_info(ifile, jfile))
            except FileNotFoundError as e:
                print (e)
                irow.append(0.)
        score_matrix.append(irow)

    # Find best score per row
    with open("list1.txt", 'w') as f_rows:
        with open("list2.txt", 'w') as f_cols:
            for irow in range(len(score_matrix)):
                # Find the couples that match the most according to the scores
                max_score = max(score_matrix[irow])
                max_idx_list = [i for i, j in enumerate(score_matrix[irow]) if j == max_score]

                if max_score > 0.:
                    for iidx in max_idx_list:
                        f_rows.write(str(list_of_files_rows[irow]) + "\n")
                        f_cols.write(str(list_of_files_cols[iidx]) + "\n")
    f_rows.close()
    f_cols.close()



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
