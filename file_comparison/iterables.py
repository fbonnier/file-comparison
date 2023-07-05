# Numpy
import numpy as np

from collections.abc import Iterable
import neo.io
# import file_comparison.stats as stats
# import json
import file_comparison.report_generator
import file_comparison.neo
import file_comparison.npz

known_types = [np.lib.npyio.NpzFile, np.ndarray, neo.core.block.Block, neo.core.Segment, str, bytes, list, dict, bool, float, int, neo.core.spiketrain.SpikeTrain, neo.core.analogsignal.AnalogSignal]

container_types = [np.lib.npyio.NpzFile, np.ndarray, neo.core.block.Block, neo.core.Segment, list, dict, neo.core.spiketrain.SpikeTrain, neo.core.analogsignal.AnalogSignal]

neo_container_types = [neo.core.spiketrain.SpikeTrain, neo.core.analogsignal.AnalogSignal]

iterable_container_types = [list]

values_type = [str, bytes, bool, float, int]

def is_iterable_container (container):
    if type(container) in container_types:
        return True
    return False

def is_neo_container (container):
    if type(container) in neo_container_types:
        return True
    return False

def get_iterable_container (container):
    if is_iterable_container (container):
        if is_neo_container (container):
            if type(container) == neo.core.spiketrain.SpikeTrain:
                return container.spiketrains
            
            return 
        if is_iterable_container (container):
            return container
    return None

def contains_values (container):
    if is_iterable_container(container):
        for item in get_iterable_container (container):
            pass
    return False

def compare_lists (list1:list, list2:list, comparison_path: str, block_diff: dict ):

    print ("iterable_are_equal List")
    # block_diff["log"].append(comparison_path+str(type(list1)))
    if len(list1) != len(list2):
        block_diff["error"].append(str(comparison_path+str(type(list1))+"->") + "List don't have same length")
        block_diff["nerrors"] += 1

    # Check type of list's elements
    contains_containers = False
    for id_ilist in range(min(len(list1), len(list2))):
        if is_iterable_container(list1[id_ilist]) or is_iterable_container(list2[id_ilist]):
            contains_containers = True
    
    if contains_containers:
        for id_ilist in range(min(len(list1), len(list2))):
            block_diff = iterable_are_equal (list1[id_ilist], list2[id_ilist], comparison_path+str(type(list1))+"->", block_diff)
    else:
        block_diff["report"].append(file_comparison.report_generator.compute_1list_difference(origin=list1, new=list2))
    
    return block_diff

def compare_dicts (original_item, new_item, comparison_path, block_diff):
    keys_to_avoid = []
    common_keys = []
    # block_diff["log"].append (comparison_path+str(type(original_item)))
    print ("iterable_are_equal Dict")


    for ikey in original_item.keys():
        if not ikey in new_item:
            keys_to_avoid.append(ikey)

    for ikey in new_item.keys():
        if not ikey in original_item:
            keys_to_avoid.append(ikey)

    common_keys = original_item.keys() - keys_to_avoid

    if len(keys_to_avoid) > 0:
        block_diff["error"].append(str(comparison_path+str(type(original_item))+"->KeysAvoided") +  str(keys_to_avoid))
        block_diff["nerrors"] += len(keys_to_avoid)
        block_diff["nvalues"] += len(keys_to_avoid)

    # Iterate on items of original_item and new_item
    for item in common_keys:
        block_diff = iterable_are_equal(original_item[item], new_item[item], comparison_path+str(type(original_item))+"->"+item+"->", block_diff)
        
    return block_diff
    

# def compare_numpy_arrays (original_item, new_item, comparison_path, block_diff):

#     block_diff["log"].append(comparison_path+str(type(original_item)))
#     block_diff["nvalues"] += len(original_item)
#     block_diff["nerrors"] += abs(len(original_item) - len(new_item))
    
#     # Check sizes
#     # TODO

#     # Check data types
#     # TODO

#     block_diff["report"].append(file_comparison.report_generator.compute_1list_difference(origin=original_item, new=new_item))
    
#     # Add errors and logs
#     # TODO
#     block_diff["nerrors"] += len(original_item) - len(new_item)
    
#     # block_diff = iterable_are_equal(original_item.tolist(), new_item.tolist(), comparison_path+str(type(original_item))+"->", block_diff)

#     return block_diff

# def compare_numpy_npz (original_item, new_item, comparison_path, block_diff):

#     keys_to_avoid = []
#     common_keys = []

#     # Check keys_to_avoid# # TODO
#     for ikey in original_item.files:
#         if not ikey in new_item.files:
#             keys_to_avoid.append(ikey)
#         elif not ikey in common_keys:
#             common_keys.append(ikey)

#     for ikey in new_item.files:
#         if not ikey in original_item.files:
#             keys_to_avoid.append(ikey)
#         elif not ikey in common_keys:
#             common_keys.append(ikey)

#     # common_keys = original_item.files - keys_to_avoid
#     if len(keys_to_avoid) > 0:
#         block_diff["error"].append(str(comparison_path+str(type(original_item))+"->KeysAvoided") + str( keys_to_avoid))
#         block_diff["nerrors"] += len(keys_to_avoid)
#         block_diff["nvalues"] += len(keys_to_avoid)

#     # Iterate on keys
#     for ivar in common_keys:
#         block_diff = iterable_are_equal(original_item[ivar], new_item[ivar], comparison_path+str(type(original_item))+"->"+str(ivar)+"->", block_diff)
#     return block_diff


# 4
# def compute_score (number_of_errors, number_of_values):
#     #TODO Catch Exception instead of assert
#     assert number_of_values > 0, "No data to compare, score is divided by 0"
#     print ("Number of errors = " + str (number_of_errors))
#     print ("Number of values = " + str (number_of_values))
#     # print ("Number of failures = " + str (len(self.all_failures)) + "\n")

#     score = 100. - (number_of_errors*100./number_of_values)

#     return (score)

# 3
# def compute_differences_report (original_file, new_file):

#     block_diff = {"report": [], "nerrors": 0, "nvalues": 0, "log": [], "error": []}
#     comparison_path = "R"
#     try:
#         original_data = np.load(original_file["path"], allow_pickle=original_file["allow_pickle"], encoding=original_file["encoding"])
#         new_data = np.load(new_file["path"], allow_pickle=new_file["allow_pickle"], encoding=new_file["encoding"])

#         block_diff = iterable_are_equal (original_data, new_data, comparison_path, block_diff)
#         # print (block_diff)
#         # print ("\n")

#     except Exception as e:
#         block_diff["error"].append("NPZ compute_differences_report: " + str(e))
#         block_diff["nerrors"] += 1

#     return block_diff

# 2
# def check_file_formats (filepath):
#     try:
#         np.load(filepath, allow_pickle=True)
#         return True, None
#     except Exception as e:
#         print ("Error " + str(type(e)) + " :: NPZ method: " + str(e))
#         return False, str(e)

def iterable_are_equal (original_item, new_item, comparison_path, block_diff):
    
    if (type (original_item) not in known_types or type(new_item) not in known_types):
        # Return error, unkown type
        block_diff["log"].append(comparison_path + " " + str(type(original_item)) + " " + str(type(new_item)))
        block_diff ["error"].append(comparison_path + " " + str(type(original_item)) + " " + str(type(new_item)) + " are not in KNOWN Types")
        block_diff["nerrors"]+=1
        block_diff["nvalues"]+=1
        print ("iterable_are_equal unknown types")

    #############   NUMPY.NPZ.Files  #################
    # Convert npz files into compatible arrays
    if ((type(original_item) == np.lib.npyio.NpzFile) and (type(new_item) == np.lib.npyio.NpzFile)):

        print ("iterable_are_equal NPZ type")

        block_diff = file_comparison.npz.compare_numpy_npz (original_item, new_item, comparison_path+str(type(original_item))+"->", block_diff)

    #############   NUMPY.arrays  #################
    # Convert numpy arrays into compatible arrays
    elif ((type(original_item) == np.ndarray) and (type(new_item) == np.ndarray)):
        print ("iterable_are_equal Numpy Array")

        # # Check type similar
        # if (original_item.dtype != new_item.dtype):
        #     block_diff["error"].append(comparison_path+str(type(original_item)) + ": Different data types")
        #     block_diff["nerrors"] += abs(len(original_item))
        # else:
            # Check element types are primitive types
            # if (original_item.dtype not in container_types):
            #     print ("iterable_are_equal Numpy Array not in container types:  " + str(original_item.dtype))
            #     block_diff = file_comparison.npz.compare_numpy_arrays (original_item, new_item, comparison_path+str(type(original_item))+"->", block_diff)
            # else:
                # print ("iterable_are_equal Numpy Array type " + str(original_item.dtype))
                
        # Check array length
        if len(original_item) - len(new_item):
            block_diff["error"].append (comparison_path+str(type(original_item)) + ": Different size, missing data")
            block_diff["nerrors"] += abs(len(original_item) - len(new_item))

        for id_ilist in range(min(len(original_item), len(new_item))):
            block_diff = iterable_are_equal (original_item[id_ilist], new_item[id_ilist], comparison_path+str(type(original_item))+"->", block_diff)


    #############   NEO.BLOCK   ###################
    # TODO
    elif (type(original_item) == neo.core.block.Block) and (type(new_item) == neo.core.block.Block):
        # TODO
        print ("iterable_are_equal NEO Block")
        block_diff = file_comparison.neo.compare_neo_blocks (original_item, new_item, comparison_path+str(original_item.name)+str(type(original_item))+"->", block_diff)

    ############    NEO.SEGMENT ##################
    # TODO
    elif (type(original_item) == neo.core.Segment) and (type(new_item) == neo.core.Segment):
        print ("iterable_are_equal NEO Segment")
        block_diff = file_comparison.neo.compare_segments(original_item, new_item, comparison_path+str(original_item.name)+str(type(original_item))+"->", block_diff)
        
    elif ((isinstance(original_item, Iterable)) and (isinstance(new_item, Iterable)) and (type(original_item)!=str) and (type(original_item)!= bytes) ):


        print ("iterable_are_equal Iterable type")
        #################   LIST    ###################
        if ((type(original_item) == list) and (type(new_item) == list)):
            # Check array length
            if len(original_item) - len(new_item):
                block_diff["error"].append (comparison_path+str(type(original_item)) + ": Different size, missing data")
                block_diff["nerrors"] += abs(len(original_item) - len(new_item))
            
            for id_ilist in range(min(len(original_item), len(new_item))):
                block_diff = iterable_are_equal (original_item[id_ilist], new_item[id_ilist], comparison_path+str(type(original_item))+"->", block_diff)
            
        #################   DICT    ###################
        # Check if original_item and new_item provide keys to check keys
        elif ((type(original_item) == dict) and (type(new_item) == dict)):
            block_diff = compare_dicts (original_item, new_item, comparison_path+str(type(original_item))+"->", block_diff)
        else:
            block_diff["error"].append(comparison_path+str(type(original_item)) + " iterable not supported")
            block_diff["nerrors"] += 1
            

    # If original_item and new_item are not iterable (are values)
    else :
        block_diff["nvalues"] += 1
        # if values are not equal
        if (original_item != new_item):
            block_delta = file_comparison.report_generator.compute_1el_difference (original_item, new_item)
            block_delta["log"].append(str(comparison_path+str(type(original_item))+"->"+str(original_item)))
            block_diff["report"].append(block_delta)
            block_diff["nerrors"] += 1
        
    return block_diff
