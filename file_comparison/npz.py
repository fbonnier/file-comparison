# Numpy
import numpy as np

from collections.abc import Iterable
import neo.io
import json
import file_comparison.report_generator as rg
import file_comparison.neo as fcneo


known_types = [np.lib.npyio.NpzFile, np.ndarray, neo.core.block.Block, neo.core.Segment, str, bytes, list, dict, bool, float, int, neo.core.spiketrain.SpikeTrain, neo.core.analogsignal.AnalogSignal,]


# all_failures = {}
# nb_values_total = 0
# nb_errors = 0

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
    nb_errors = 0
    nb_values_total = 0
    all_failures = {}

    with np.load(file1["path"], allow_pickle=file1["allow_pickle"], encoding=file1["encoding"]) as data_1, np.load(file2["path"], allow_pickle=file2["allow_pickle"], encoding=file2["encoding"]) as data_2:
        # data_1_list = data_1.files
        # data_2_list = data_2.files
        comparison_path="R"
        all_failures, nb_errors, nb_values_total = iterable_are_equal (data_1, data_2, comparison_path, all_failures, nb_errors, nb_values_total)
        # Print failures Line-by-Line
        # print(json.dumps(all_failures, indent=4))

    # ratio =  compute_ratio()
    # print ("Ratio = " + str(ratio) + " %")
    return all_failures, nb_errors, nb_values_total

# 2
def check_file_formats (filepath):
    try:
        np.load(filepath, allow_pickle=True)
        return True, None
    except Exception as e:
        print ("Error " + str(type(e)) + " :: NPZ method: " + str(e))
        return False, str(e)

def iterable_are_equal (item1, item2, comparison_path, all_failures, nb_errors, nb_values_total):
    keys_to_avoid = []
    common_keys = []

    if (type (item1) not in known_types or type(item2) not in known_types):
        # Return error, unkown type
        print (comparison_path + " " + str(type(item1)) + " " + str(type(item2)) + " are not in KNOWN Types\n")
        all_failures [str(comparison_path)+ " " + str(type(item1))] = "Unknown Type"
        nb_errors+=1
        nb_values_total+=1
        return all_failures, nb_errors, nb_values_total

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
            nb_errors += len(keys_to_avoid)
            nb_values_total += len(keys_to_avoid)

        # Iterate on keys
        for ivar in common_keys:
            all_failures, nb_errors, nb_values_total = iterable_are_equal(item1[ivar], item2[ivar], comparison_path+str(type(item1))+"->"+str(ivar)+"->", all_failures, nb_errors, nb_values_total)
            return all_failures, nb_errors, nb_values_total

    #############   NUMPY.arrays  #################
    # Convert numpy arrays into compatible arrays
    elif ((type(item1) == np.ndarray) and (type(item2) == np.ndarray)):
        all_failures, nb_errors, nb_values_total = iterable_are_equal(item1.tolist(), item2.tolist(), comparison_path+str(type(item1))+"->", all_failures, nb_errors, nb_values_total)
        return all_failures, nb_errors, nb_values_total

    #############   NEO.BLOCK   ###################
    # TODO
    elif (type(item1) == neo.core.block.Block) and (type(item2) == neo.core.block.Block):
        all_failures, nb_errors, nb_values_total = fcneo.compare_neo_blocks (item1, item2, comparison_path+str(item1.name)+str(type(item1))+"->", all_failures, nb_errors, nb_values_total)
        return all_failures, nb_errors, nb_values_total
        # Convert neo.blocks into compatible arrays
        # if (len(item1.segments) != len(item2.segments)):
        #     all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of segments don't have same length"

        # for ivar in range( min ( len(item1.segments), len(item2.segments))):
        #     all_failures, nb_errors, nb_values_total = iterable_are_equal(item1.segments[ivar], item2.segments[ivar], comparison_path+str(item1.name)+str(type(item1))+"->", all_failures, nb_errors, nb_values_total)

    ############    NEO.SEGMENT ##################
    # TODO
    elif (type(item1) == neo.core.Segment) and (type(item2) == neo.core.Segment):
        all_failures, nb_errors, nb_values_total = fcneo.compare_segments(item1, item2, comparison_path+str(item1.name)+str(type(item1))+"->",all_failures, nb_errors, nb_values_total)
        return all_failures, nb_errors, nb_values_total
        #############   AnalogSignal    ##############
        # if (len(item1.analogsignals) != len(item2.analogsignals)):
        #     all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of AnalogSignal don't have same length"
        #
        # if (len(item1.analogsignals)>0):
        #     for ivar in range (len(item1.analogsignals)):
        #         all_failures, nb_errors, nb_values_total = iterable_are_equal (item1.analogsignals[ivar], item2.analogsignals[ivar], comparison_path+str(item1.name)+str(type(item1))+"->", all_failures, nb_errors, nb_values_total)

        #############   SpikeTrain    ##############
        # if (len(item1.spiketrains) != len(item2.spiketrains)):
        #     all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of SpikeTrain don't have same length"
        #
        # if (len(item1.spiketrains)>0):
        #     for ivar in range (len(item1.spiketrains)):
        #         iterable_are_equal (item1.spiketrains[ivar], item2.spiketrains[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   Event    ##############
        # if (len(item1.events) != len(item2.events)):
        #     all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of Event don't have same length"
        #
        # if (len(item1.events)>0):
        #     for ivar in range (len(item1.events)):
        #         iterable_are_equal (item1.events[ivar], item2.events[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   Epoch    ##############
        # if (len(item1.epochs) != len(item2.epochs)):
        #     all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of Epoch don't have same length"
        #
        # if (len(item1.epochs)>0):
        #     for ivar in range (len(item1.epochs)):
        #         iterable_are_equal (item1.epochs[ivar], item2.epochs[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   IrregularlySampledSignal    ##############
        # if (len(item1.irregularlysampledsignals) != len(item2.irregularlysampledsignals)):
        #     all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of IrregularlySampledSignal don't have same length"
        #
        # if (len(item1.irregularlysampledsignals)>0):
        #     for ivar in range (len(item1.irregularlysampledsignals)):
        #         iterable_are_equal (item1.irregularlysampledsignals[ivar], item2.irregularlysampledsignals[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

    elif ((isinstance(item1, Iterable)) and (isinstance(item2, Iterable)) and (type(item1)!=str) and (type(item1)!= bytes) ):

        #################   LIST    ###################
        if ((type(item1) == list) and (type(item2) == list)):
            if len(item1) != len(item2):
                all_failures[str(comparison_path+str(type(item1))+"->")] = "List don't have same length"
            for id_ilist in range(min(len(item1), len(item2))):
                all_failures, nb_errors, nb_values_total = iterable_are_equal (item1[id_ilist], item2[id_ilist], comparison_path+str(type(item1))+"->", all_failures, nb_errors, nb_values_total)
                return all_failures, nb_errors, nb_values_total
        #################   DICT    ###################
        # Check if item1 and item2 provide keys to check keys
        if ((type(item1) == dict) and (type(item2) == dict)):
            keys_to_avoid = []
            common_keys = []

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
                nb_errors += 1
                nb_values_total += 1

            # Iterate on items of item1 and item2
            for item in common_keys:
                all_failures, nb_errors, nb_values_total = iterable_are_equal(item1[item], item2[item], comparison_path+str(type(item1))+"->"+item+"->", all_failures, nb_errors, nb_values_total)
                return all_failures, nb_errors, nb_values_total

    # If item1 and item2 are not iterable (are values)
    else :
        nb_values_total += 1
        # if values are not equal
        if (item1 != item2):
            delta = rg.compute_1el_difference (item1, item2)
            all_failures[str(comparison_path+str(type(item1))+"->"+str(item1))] = delta
            nb_errors += 1
            return all_failures, nb_errors, nb_values_total

# def npz_values (f1_path, f2_path):
#     with open(f1_path, "r") as f1:
#         with open(f2_path, "r") as f2:
#             linesf1 = f1.readlines()
#             linesf2 = f2.readlines()
#             assert(len(linesf1) == len(linesf2))
#             for idx in range(len(linesf1)):
#
#                 # Set default filename
#                 filename1 = linesf1[idx].split("\n")[0]
#                 filename2 = linesf2[idx].split("\n")[0]
#
#                 ratio, file_diffs = npz_single(filename1, filename2, buffer_size)
#
#     return ratio, all_failures

# def npz_single (f1_path, f2_path):
#
#     ## Check if both files are NPZ files
#     if ((not f1_path.endswith(".npz")) or (not f2_path.endswith(".npz"))):
#         print ("Error :: NPZ value comparison needs two NPZ files")
#         exit (1)
#
#     with np.load(f1_path, allow_pickle=True) as data_1:
#         with np.load(f2_path, allow_pickle=True) as data_2:
#             data_1_list = data_1.files
#             data_2_list = data_2.files
#             comparison_path="R"
#             iterable_are_equal (data_1, data_2, comparison_path)
#             # Print failures Line-by-Line
#             # print(json.dumps(all_failures, indent=4))
#
#     ratio =  compute_ratio()
#     # print ("Ratio = " + str(ratio) + " %")
#     return ratio, all_failures
