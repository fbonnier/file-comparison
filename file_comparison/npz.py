# Numpy
import numpy as np

from collections.abc import Iterable
import neo.io
import json
import file_comparison.report_generator as rg
import file_comparison.neo as fcneo


known_types = [np.lib.npyio.NpzFile, np.ndarray, neo.core.block.Block, neo.core.Segment, str, bytes, list, dict, bool, float, int, neo.core.spiketrain.SpikeTrain, neo.core.analogsignal.AnalogSignal]

def compare_lists (list1:list, list2:list, comparison_path: str, block_diff: dict):

    block_diff["log"].append(comparison_path+str(type(list1)))
    if len(list1) != len(list2):
        block_diff["report"][str(comparison_path+str(type(list1))+"->")] = "List don't have same length"
        block_diff["nerrors"] += 1
    
    for id_ilist in range(min(len(list1), len(list2))):
        block_diff = iterable_are_equal (list1[id_ilist], list2[id_ilist], comparison_path+str(type(list1))+"->", block_diff)
    
    return block_diff

def compare_dicts (item1, item2, comparison_path, block_diff):
    keys_to_avoid = []
    common_keys = []
    block_diff["log"].append (comparison_path+str(type(item1)))

    for ikey in item1.keys():
        if not ikey in item2:
            keys_to_avoid.append(ikey)

    for ikey in item2.keys():
        if not ikey in item1:
            keys_to_avoid.append(ikey)

    common_keys = item1.keys() - keys_to_avoid

    if len(keys_to_avoid) > 0:
        block_diff["report"][str(comparison_path+str(type(item1))+"->KeysAvoided")] = keys_to_avoid
        block_diff["nerrors"] += len(keys_to_avoid)
        block_diff["nvalues"] += len(keys_to_avoid)

    # Iterate on items of item1 and item2
    for item in common_keys:
        block_diff = iterable_are_equal(item1[item], item2[item], comparison_path+str(type(item1))+"->"+item+"->", block_diff)
        
    return block_diff
    

def compare_numpy_arrays (item1, item2, comparison_path, block_diff):

    block_diff["log"].append(comparison_path+str(type(item1)))
    
    block_diff = iterable_are_equal(item1.tolist(), item2.tolist(), comparison_path+str(type(item1))+"->", block_diff)

    return block_diff

def compare_numpy_npz (item1, item2, comparison_path, block_diff):

    keys_to_avoid = []
    common_keys = []

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
    if len(keys_to_avoid) > 0:
        block_diff["report"][str(comparison_path+str(type(item1))+"->KeysAvoided")] = keys_to_avoid
        block_diff["nerrors"] += len(keys_to_avoid)
        block_diff["nvalues"] += len(keys_to_avoid)

    # Iterate on keys
    for ivar in common_keys:
        block_diff = iterable_are_equal(item1[ivar], item2[ivar], comparison_path+str(type(item1))+"->"+str(ivar)+"->", block_diff)
    return block_diff


# 4
def compute_score (number_of_errors, number_of_values):
    #TODO Catch Exception instead of assert
    assert number_of_values > 0, "No data to compare, score is divided by 0"
    print ("Number of errors = " + str (number_of_errors))
    print ("Number of values = " + str (number_of_values))
    # print ("Number of failures = " + str (len(self.all_failures)) + "\n")

    score = 100. - (number_of_errors*100./number_of_values)

    return (score)

# 3
def compute_differences_report (file1, file2):

    block_diff = {"report": {}, "nerrors": 0, "nvalues": 0, "log": [], "error": []}
    comparison_path = "R"
    try:
        data1 = np.load(file1["path"], allow_pickle=file1["allow_pickle"], encoding=file1["encoding"])
        data2 = np.load(file2["path"], allow_pickle=file2["allow_pickle"], encoding=file2["encoding"])

        block_diff = iterable_are_equal (data1, data2, comparison_path, block_diff)

    except Exception as e:
        block_diff["error"].append("NPZ compute_differences_report: " + str(e))
        block_diff["nerrors"] += 1

    return block_diff

# 2
def check_file_formats (filepath):
    try:
        np.load(filepath, allow_pickle=True)
        return True, None
    except Exception as e:
        print ("Error " + str(type(e)) + " :: NPZ method: " + str(e))
        return False, str(e)

def iterable_are_equal (item1, item2, comparison_path, block_diff):
    
    if (type (item1) not in known_types or type(item2) not in known_types):
        # Return error, unkown type
        block_diff["log"].append(comparison_path + " " + str(type(item1)) + " " + str(type(item2)))
        block_diff ["error"].append(comparison_path + " " + str(type(item1)) + " " + str(type(item2)) + " are not in KNOWN Types")
        block_diff["nerrors"]+=1
        block_diff["nvalues"]+=1

    #############   NUMPY.NPZ.Files  #################
    # Convert npz files into compatible arrays
    if ((type(item1) == np.lib.npyio.NpzFile) and (type(item2) == np.lib.npyio.NpzFile)):
        
        block_diff = compare_numpy_npz (item1, item2, comparison_path+str(type(item1))+"->", block_diff)

    #############   NUMPY.arrays  #################
    # Convert numpy arrays into compatible arrays
    elif ((type(item1) == np.ndarray) and (type(item2) == np.ndarray)):
        block_diff = compare_numpy_arrays (item1, item2, comparison_path+str(type(item1))+"->", block_diff)

    #############   NEO.BLOCK   ###################
    # TODO
    elif (type(item1) == neo.core.block.Block) and (type(item2) == neo.core.block.Block):
        # TODO
        block_diff = fcneo.compare_neo_blocks (item1, item2, comparison_path+str(item1.name)+str(type(item1))+"->", block_diff)

    ############    NEO.SEGMENT ##################
    # TODO
    elif (type(item1) == neo.core.Segment) and (type(item2) == neo.core.Segment):
        block_diff = fcneo.compare_segments(item1, item2, comparison_path+str(item1.name)+str(type(item1))+"->", block_diff)
        
    elif ((isinstance(item1, Iterable)) and (isinstance(item2, Iterable)) and (type(item1)!=str) and (type(item1)!= bytes) ):

        #################   LIST    ###################
        if ((type(item1) == list) and (type(item2) == list)):
            block_diff = compare_lists (item1, item2, comparison_path+str(type(item1))+"->", block_diff)
            
        #################   DICT    ###################
        # Check if item1 and item2 provide keys to check keys
        elif ((type(item1) == dict) and (type(item2) == dict)):
            block_diff = compare_dicts (item1, item2, comparison_path+str(type(item1))+"->", block_diff)
        else:
            block_diff["error"].append(comparison_path+str(type(item1)) + " iterable not supported")
            block_diff["nerrors"] += 1
            

    # If item1 and item2 are not iterable (are values)
    else :
        block_diff["nvalues"] += 1
        # if values are not equal
        if (item1 != item2):
            block_delta = rg.compute_1el_difference (item1, item2)
            block_diff["report"][str(comparison_path+str(type(item1))+"->"+str(item1))] = block_delta
            block_diff["nerrors"] += 1
        
    return block_diff
