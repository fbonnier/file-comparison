# List of comparison methods to compare two files and retrieve closest ones

# Fuzzy String comparisons
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

# Numpy
import numpy as np

from collections.abc import Iterable
import neo.io
import json

import os

# Byte processing
# from bitstring import BitArray

# Number of bytes in the buffer to compare
BYTE_BUFFER = 64

all_failures = {}
known_types = [np.lib.npyio.NpzFile, np.ndarray, neo.core.block.Block, neo.core.Segment, str, bytes, list, dict, bool, float, int, neo.core.spiketrain.SpikeTrain, neo.core.analogsignal.AnalogSignal,]

def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

def iterable_are_equal (item1, item2, comparison_path):
    keys_to_avoid = []
    common_keys = []
    # print (comparison_path)

    if (type (item1) not in known_types or type(item2) not in known_types):
        print (comparison_path + " " + str(type(item1)) + " " + str(type(item2)))

    #############   NUMPY.NPZ.Files  #################
    # Convert npz files into compatible arrays
    if ((type(item1) == np.lib.npyio.NpzFile) and (type(item2) == np.lib.npyio.NpzFile)):
        # Check keys_to_avoid# # TODO
        for ikey in item1.files:
            if not ikey in item2.files:
                keys_to_avoid.append(ikey)
            elif not ikey in common_keys:
                common_keys.append(ikey)

        for ikey in item2.files:
            if not ikey in item1.files:
                keys_to_avoid.append(ikey)
            elif not ikey in common_keys:
                common_keys.append(ikey)

        # common_keys = item1.files - keys_to_avoid
        if len(keys_to_avoid) >0:
            all_failures[str(comparison_path+str(type(item1))+"->KeysAvoided")] = keys_to_avoid

        # Iterate on keys
        for ivar in common_keys:
            iterable_are_equal(item1[ivar], item2[ivar], comparison_path+str(type(item1))+"->"+str(ivar)+"->")

    #############   NUMPY.arrays  #################
    # Convert numpy arrays into compatible arrays
    elif ((type(item1) == np.ndarray) and (type(item2) == np.ndarray)):
        iterable_are_equal(item1.tolist(), item2.tolist(), comparison_path+str(type(item1))+"->")

    #############   NEO.BLOCK   ###################
    # TODO
    elif (type(item1) == neo.core.block.Block) and (type(item2) == neo.core.block.Block):
        # Convert neo.blocks into compatible arrays
        if (len(item1.segments) != len(item2.segments)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of segments don't have same length"

        for ivar in range( len(item1.segments)):
            iterable_are_equal(item1.segments[ivar], item2.segments[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

    ############    NEO.SEGMENT ##################
    # TODO
    elif (type(item1) == neo.core.Segment) and (type(item2) == neo.core.Segment):
        #############   AnalogSignal    ##############
        if (len(item1.analogsignals) != len(item2.analogsignals)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of AnalogSignal don't have same length"

        if (len(item1.analogsignals)>0):
            for ivar in range (len(item1.analogsignals)):
                iterable_are_equal (item1.analogsignals[ivar], item2.analogsignals[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   SpikeTrain    ##############
        if (len(item1.spiketrains) != len(item2.spiketrains)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of SpikeTrain don't have same length"

        if (len(item1.spiketrains)>0):
            for ivar in range (len(item1.spiketrains)):
                iterable_are_equal (item1.spiketrains[ivar], item2.spiketrains[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   Event    ##############
        if (len(item1.events) != len(item2.events)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of Event don't have same length"

        if (len(item1.events)>0):
            for ivar in range (len(item1.events)):
                iterable_are_equal (item1.events[ivar], item2.events[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   Epoch    ##############
        if (len(item1.epochs) != len(item2.epochs)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of Epoch don't have same length"

        if (len(item1.epochs)>0):
            for ivar in range (len(item1.epochs)):
                iterable_are_equal (item1.epochs[ivar], item2.epochs[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   IrregularlySampledSignal    ##############
        if (len(item1.irregularlysampledsignals) != len(item2.irregularlysampledsignals)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of IrregularlySampledSignal don't have same length"

        if (len(item1.irregularlysampledsignals)>0):
            for ivar in range (len(item1.irregularlysampledsignals)):
                iterable_are_equal (item1.irregularlysampledsignals[ivar], item2.irregularlysampledsignals[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

    elif ((isinstance(item1, Iterable)) and (isinstance(item2, Iterable)) and (type(item1)!=str) and (type(item1)!= bytes) ):


        #################   LIST    ###################
        if ((type(item1) == list) and (type(item2) == list)):
            if len(item1) != len(item2):
                all_failures[str(comparison_path+str(type(item1))+"->")] = "List don't have same length"
            else:
                for id_ilist in range(len(item1)):
                    iterable_are_equal (item1[id_ilist], item2[id_ilist], comparison_path+str(type(item1))+"->")

        #################   DICT    ###################
        # Check if item1 and item2 provide keys to check keys
        if ((type(item1) == dict) and (type(item2) == dict)):

            for ikey in item1.keys():
                if not ikey in item2:
                    # print ("%s not present in one dataset" %(comparison_path+str(type(item1))+"->" +"->"+ str(ikey)))
                    keys_to_avoid.append(ikey)

            for ikey in item2.keys():
                if not ikey in item1:
                    # print ("%s not present in one dataset" %(comparison_path+str(type(item1))+"->"+"->"+str(ikey)))
                    keys_to_avoid.append(ikey)

            common_keys = item1.keys() - keys_to_avoid
            if len(keys_to_avoid) >0:
                all_failures[str(comparison_path+str(type(item1))+"->KeysAvoided")] = keys_to_avoid

            # Iterate on items of item1 and item2
            for item in common_keys:
                iterable_are_equal(item1[item], item2[item], comparison_path+str(type(item1))+"->"+item+"->")


    # If item1 and item2 are not iterable (are values)
    elif (item1 != item2):
        all_failures[str(comparison_path+str(type(item1))+"->"+str(item1))] = "(delta= TODO)"

    # elif type(item1) not in [int, float, bool, str, type(None), bytes]:
    #         print ("Item1 " + str(comparison_path) + str(type(item1)))
    #         print ("Item2 " + str(comparison_path) + str(type(item2)))



# Levenshtein Distance
# INPUT: s1, s2: strings of bytes, arrays of bytes
# OUTPUT: Score
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]



def levenshtein_files(f1_path, f2_path):
    ####################
    ## NOT WORKING ##
    ####################

    # Open files in byte mode
    # Cut the files into N bytes with N=64
    # Compatible with Python 2.6 and Python 3.x
    # ref: https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read(BYTE_BUFFER)
        f2_byte = f2.read(BYTE_BUFFER)
        # HIGHER_SCORE = 0

        while f1_byte and f2_byte:
            # Run Levenshtein Distance computation
            score = levenshtein(str(f1_byte), str(f2_byte))
            # if (HIGHER_SCORE < score):
                # HIGHER_SCORE = score
            print ("Score = " + str(score))

            f1_byte = f1.read(BYTE_BUFFER)
            f2_byte = f2.read(BYTE_BUFFER)


        # Last comparison in case the files closed before filling 64 bytes arrays
        if len(str(f1_byte)):
            score = levenshtein(str(f1_byte), str(f2_byte))
            print ("Last score for arrays of size " + str(len(str(f1_byte))) + " " + str(len(str(f2_byte))) + " = " + str(score))

def fuzzy_files_light(f1_path, f2_path):

    # Total Score
    TOTAL_SCORE = 0
    # Number of buffer used
    NBUFFER = 0

    # Open files in byte mode
    # Cut the files into N bytes with N=64
    # Compatible with Python 2.6 and Python 3.x
    # ref: https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read(BYTE_BUFFER)
        f2_byte = f2.read(BYTE_BUFFER)

        while f1_byte and f2_byte:
            # Run Levenshtein Distance computation
            score = fuzz.ratio(str(f1_byte), str(f2_byte))

            NBUFFER += 1
            TOTAL_SCORE += score
            # Initialize strings

            f1_byte = f1.read(BYTE_BUFFER)
            f2_byte = f2.read(BYTE_BUFFER)

        # Last comparison in case the files closed before filling 64 bytes arrays
        if len(str(f1_byte)):
            score = fuzz.ratio(str(f1_byte), str(f2_byte))
            NBUFFER += 1
            TOTAL_SCORE += score
            # print ("Last score for arrays of size " + str(len(f1_str)) + " " + str(len(f2_str)) + " = " + str(score))
        print ("Total = " + str(TOTAL_SCORE))
        print ("Total buffer = " + str(NBUFFER))
        print ("Total ratio = " + str(TOTAL_SCORE / NBUFFER) + " %")

def fuzzy_files_light_entire_file(f1_path, f2_path):

    # Total Score
    TOTAL_SCORE = 0
    # Number of buffer used
    NBUFFER = 0

    # Open files in byte mode
    # Cut the files into N bytes with N=64
    # Compatible with Python 2.6 and Python 3.x
    # ref: https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read()
        f2_byte = f2.read()

        # while f1_byte and f2_byte:
        # Run Levenshtein Distance computation
        score = fuzz.ratio(str(f1_byte), str(f2_byte))

        NBUFFER += 1
        TOTAL_SCORE += score
            # Initialize strings

            # f1_byte = f1.read(BYTE_BUFFER)
            # f2_byte = f2.read(BYTE_BUFFER)

        # Last comparison in case the files closed before filling 64 bytes arrays
        # if len(str(f1_byte)):
        #     score = fuzz.ratio(str(f1_byte), str(f2_byte))
        #     NBUFFER += 1
        #     TOTAL_SCORE += score
            # print ("Last score for arrays of size " + str(len(f1_str)) + " " + str(len(f2_str)) + " = " + str(score))
        print ("Total = " + str(TOTAL_SCORE))
        print ("Total buffer = " + str(NBUFFER))
        print ("Total ratio = " + str(TOTAL_SCORE / NBUFFER) + " %")

## Computes Hamming Distance between seq1 and seq2
#  INPUT: seq1, seq2: byte buffers
#  OUTPUT: distance (int)
def hamming_distance (seq1, seq2):
    # https://cppsecrets.com/users/7927971001051161051071111161041051219710855484864103109971051084699111109/Python-Hamming-Distance.php
    count = 0
    for ibyte in range(min(len(seq1),len(seq2))):

        z = seq1[ibyte] ^ seq2[ibyte]

        while z:
            count += 1
            z &= z-1 # magic!
    count /= BYTE_BUFFER
    return count

def hamming_files(f1_path, f2_path):

    # Total Score
    TOTAL_SCORE = 0
    # Number of buffer used
    NBUFFER = 0
    # Total ratio
    TOTAL_RATIO = 0

    # Open files in byte mode
    # Cut the files into N bytes with N=64
    # Compatible with Python 2.6 and Python 3.x
    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read(BYTE_BUFFER)
        f2_byte = f2.read(BYTE_BUFFER)

        while f1_byte and f2_byte:
            # Run Hamming Distance computation
            score = hamming_distance(f1_byte, f2_byte)

            NBUFFER += 1
            TOTAL_SCORE += score
            TOTAL_RATIO += compute_ratio (score)
            # Initialize strings
            f1_byte = f1.read(BYTE_BUFFER)
            f2_byte = f2.read(BYTE_BUFFER)


        print ("Total Distance = " + str(TOTAL_SCORE))
        print ("Nb buffers = " + str(NBUFFER))
        print ("Average Distance = " + str(TOTAL_SCORE / NBUFFER))
        print ("Average Ratio = " + str(TOTAL_RATIO / NBUFFER * 100) + " %")

def nilsimsa_files (f1_path, f2_path):

    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read(BYTE_BUFFER)
        f2_byte = f2.read(BYTE_BUFFER)

        # Total Score
        TOTAL_SCORE = 0
        # Number of buffer used
        NBUFFER = 0
        # Total ratio
        TOTAL_RATIO = 0

        while f1_byte and f2_byte:

            # Computes the hash value of the buffer
            nil1 = Nilsimsa(f1_byte)
            nil2 = Nilsimsa(f2_byte)

            # Computes the comparison between hashed buffers
            score_nilsimsa = compare_digests (nil1.hexdigest(), nil2.hexdigest())
            TOTAL_RATIO += compute_ratio (score_nilsimsa)
            # print ("Score Nilsimsa " + str(score_nilsimsa))
            TOTAL_SCORE += 128 - score_nilsimsa
            NBUFFER += 1

            # Initialize strings
            f1_byte = f1.read(BYTE_BUFFER)
            f2_byte = f2.read(BYTE_BUFFER)


        # Last comparison in case the files closed before filling 64 bytes arrays
        # if len(f1_str):
        #     score = fuzz.ratio (str(Nilsimsa(f1_byte).hexdigest()), str(Nilsimsa(f2_byte).hexdigest()))
        #     NBUFFER += 1
        #     TOTAL_SCORE += score
            # print ("Last score for arrays of size " + str(len(f1_str)) + " " + str(len(f2_str)) + " = " + str(score))
        print ("\nTotal Distance = " + str(TOTAL_SCORE))
        print ("Nb buffers = " + str(NBUFFER))
        print ("Average Nilsimsa Distance = " + str(TOTAL_SCORE / NBUFFER))
        print ("Average Nilsimsa Ratio = " + str(TOTAL_RATIO / NBUFFER * 100.0) + " %")


def npz_values (f1_path, f2_path):
    ## TODO

    ## Check if both files are NPZ files
    if ((not f1_path.endswith(".npz")) or (not f2_path.endswith(".npz"))):
        print ("Error :: NPZ value comparison needs two NPZ files")
        exit (1)

    with np.load(f1_path, allow_pickle=True) as data_1:
        with np.load(f2_path, allow_pickle=True) as data_2:
            data_1_list = data_1.files
            data_2_list = data_2.files
            comparison_path="R"
            iterable_are_equal (data_1, data_2, comparison_path)
            # Print failures Line-by-Line
            print(json.dumps(all_failures, indent=4))

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
