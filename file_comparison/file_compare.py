# List of comparison methods to compare two files and retrieve closest ones

# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

import os
import hashlib

adjacent_matrix_list1 = {}
adjacent_matrix_list2 = {}

def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

def get_files_from_watchdog_log (watchdog_file, is_hex=1):
    list_of_files = []
    print ("Is HEX ? " + str(is_hex))

    with open (watchdog_file, 'r') as f1:
        lines = f1.readlines()
        for irawline in lines :
            iline = irawline.split('\n')[0]
            src_dest = iline.split()
            for ifile in src_dest:
                idirname = os.path.dirname(ifile)
                ifilename = os.path.basename(ifile)
                ifilehex = ifilename
                # if not idirname:
                #     idirname = str(os.environ["WORKDIR"]) + "expected_results"
                ifilesize = os.path.getsize(ifile)
                if is_hex:
                    ifilehex = str(hashlib.md5(bytes(ifilename + str(ifilesize), encoding='utf-8')).hexdigest())
                print ("IFileName = " + idirname + "/" + ifilename)
                list_of_files.append({"url": ifile, "file": idirname + "/" + ifilehex})
    print (list_of_files)
    return list_of_files

def find_bijective (f1, f2, hex=1):

    expected_res_path = str(os.environ["WORKDIR"]) + "/expected_results/"

    # Check hexadigest file format
    # list_of_files_rows = []
    # list_of_files_cols = []

    if hex==1:
        # Read files from watchdog logs
        # The produced files
        print ("L1:")
        adjacent_matrix_list1 = get_files_from_watchdog_log (f1, True)
        print ("L2:")
        adjacent_matrix_list2 = get_files_from_watchdog_log (f2, False)

    elif hex==2:
        # Read files from watchdog logs
        print ("L1:")
        adjacent_matrix_list1 = get_files_from_watchdog_log (f1, True)
        print ("L2:")
        adjacent_matrix_list2 = get_files_from_watchdog_log (f2, True)
    else:
        # Read files from watchdog logs
        print ("L1:")
        adjacent_matrix_list1 = get_files_from_watchdog_log (f1, False)
        print ("L2:")
        adjacent_matrix_list2 = get_files_from_watchdog_log (f2, False)



    print ("\n")
    print ("adjacent_matrix_list1")
    print (adjacent_matrix_list1)
    print ("\n")
    print ("adjacent_matrix_list1")
    print (adjacent_matrix_list2)
    print ("\n")

    # Score Matrix
    score_matrix = []

    # # Loop over all files in list01 and list02 and compute a score for each write_code_location
    for ifile in adjacent_matrix_list1:
        # Gives the first row
        irow = []
        for jfile in adjacent_matrix_list2:
            try:
                irow.append (hash_from_file_info(ifile, jfile))
            except FileNotFoundError as e:
                print (e)
                irow.append(0.)
        score_matrix.append(irow)

    pairs = []

    # Find best score per row
    # with open("list1.txt", 'w') as f_rows:
    #     with open("list2.txt", 'w') as f_cols:
    for irow in range(len(score_matrix)):
        # Find the couples that match the most according to the scores
        max_score = max(score_matrix[irow])
        max_idx_list = [i for i, j in enumerate(score_matrix[irow]) if j == max_score]

        if max_score > 0.:
            for iidx in max_idx_list:
                # print (list(adjacent_matrix_list1.values())[irow])
                # f_rows.write(str(list(adjacent_matrix_list1.values())[irow]) + "\n")
                # f_cols.write(str(list(adjacent_matrix_list2.values())[iidx]) + "\n")
                ituple = tuple ((adjacent_matrix_list1[irow], adjacent_matrix_list2[iidx]))
                pairs.append (ituple)

    return pairs


##
# Parameters are pairs (arrays of 2 items)
# array[0] : original url of the file, original name
# array[1] : true path of the file on disk (hashed, moved or transformed name)
def hash_from_file_info (f1_pair, f2_pair):
    ## Hash file informations
    #   * file name
    #   * file size
    #   * file path
    url1 = f1_pair["url"]
    path1 = f1_pair["file"]
    url2 = f2_pair["url"]
    path2 = f2_pair["file"]
    print ("Dirname f1= " + os.path.dirname(path1))
    print ("Basename f1= " + os.path.basename(url1))
    print ("Size f1 = " + str(os.path.getsize(path1)))
    print ("Dirname f2= " + os.path.dirname(path2))
    print ("Basename f2= " + os.path.basename(url2))
    print ("Size f2 = " + str(os.path.getsize(path2)))
    all_info_f1 = os.path.basename(url1) + str(os.path.getsize(path1))
    all_info_f2 = os.path.basename(url2) + str(os.path.getsize(path2))
    print (all_info_f1)
    print (Nilsimsa(all_info_f1))
    print (all_info_f2)
    print (Nilsimsa(all_info_f2))
    ratio = compute_ratio (compare_digests (Nilsimsa(all_info_f1).hexdigest(), Nilsimsa(all_info_f2).hexdigest()))
    print ("FINFO Ratio = " + str(ratio*100))
    return (ratio*100)
    ## Hash is done using Nilsimsa algorithm to get strong colisions
    # f1_hash = Nilsimsa (bytes(os.path.dirname + ))


# def advice_method (adjacency_matrix)
