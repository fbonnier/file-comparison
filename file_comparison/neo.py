# Neo
from collections.abc import Iterable
import neo.io




# class NeoCompare:

#     file1 = None
#     file2 = None
#     data_file1 = {}
#     data_file2 = {}
#     differences = {}
#     missing_data = {}

#     def __init__(self, file1, file2):
#         self.file1 = file1
#         self.file2 = file2
#         # 1. Check files are supported
#         if check_file_formats (file1) and check_file_formats (file2):

#             # 2. Extract all raw data
#             extract_neo_data (file1, self.data_file1)
#             extract_neo_data (file2, self.data_file2)

#     def __compute_scores__ (self):
#         pass


#     # Root Mean Squared Error
#     def rmse (self, prod, expect):
#         self.rmse_score = sqrt(mean_squared_error(prod, expect))
#         return self.rmse_score

#     # Mean Squared Error
#     def mse (self, prod, expect):
#         prod, expect = np.array(prod), np.array(expect)
#         self.mse_score = np.square(np.subtract(prod, expect)).mean()
#         return self.mse_score

#     # Mean Absolute Percentage Error
#     def mape (self, prod, expect):
#         prod, expect = np.array(prod), np.array(expect)
#         self.mape_score = np.mean(np.abs((prod - expect) / prod)) * 100
#         return self.mape_score

def compute_score (number_of_errors, number_of_values):
    score = 100. - (number_of_errors*100./number_of_values)
    return (score)

def check_array_size_warning (array1, array2):
    # Assert blocks or segments have same size
    if len(array1) != len(array2):
        # print ("NEO Error:" + self.file1.url + self.file1.name + " and " + self.file2.url + self.file2.name + " do not have the same number of " + str(type(array1).__name__))
        print ("NEO Warning: Number of " + str(type(array1).__name__) + " are not equal: not all " + str(type(array1).__name__) + " will be compared" )

def check_file_format (filepath):
    try:
        neo.io.get_io(filepath)
        return True, None
    except Exception as e:
        print ("Error " + str(type(e)) + " :: Neo method: " + str(e))
        return False, str(e)



def extract_neo_block (block, path, data):
    # assert(len(neoblock1.segments) == len(neoblock2.segments))
    # print ("nombre de segment = " + str(len(neoblock1.segments)))
    for isegment_idx in range(len(block.segments)):
        extract_neo_segment (block.segments[isegment_idx], path + "->segment[" + str(isegment_idx) + "]", data)

    for igroup_idx in range(len(block.groups)):
        extract_neo_group (neoblock1.groups[igroup_idx], neoblock2.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]")

def extract_neo_group (group, path, data):

    for igroup_idx in range(len(group.groups)):
        extract_neo_group (group.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]", data)

    extract_neo_segment (group, path, data)

def extract_neo_data (file, data):
    try:
        file_path = file.url + file.name

        neo_reader = neo.io.get_io(file_path)

        blocks = neo_reader.read()

        for iblock_idx in range(len(blocks)):
            extract_neo_block (blocks[iblock_idx], "R->block[" + str(iblock_idx) + "]", data)
    except Exception as e:
        print ("Neo :: " + str(type(e).__name__) + " " + str(e))


def extract_neo_segment (segment, path, data):
    try:
        # Group objects
        # print (path + "->channelview")
        # print (segment1.channelview)
        for ivar_idx in range(len(segment.channelview)):
            dara[str(path+str("->channelview[" + str(ivar_idx) + "]") + "->")] = segment.channelview[ivar_idx]
    except Exception as e:
        print (type(segment.channelview))
        print (type(segment))
        print ("Error Neo :: " + str(e))

    try:
        # print (path + "->analogsignals")
        for ivar_idx in range(len(segment.analogsignals)):
            data[str(path+str("->analogsignals[" + str(ivar_idx) + "]") + "->")] = segment.analogsignals[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
    #     print (path + "->irregularlysampledsignals")
        for ivar_idx in range(len(segment.irregularlysampledsignals)):
            data[str(path+str("->irregularlysampledsignals[" + str(ivar_idx) + "]") + "->")] = segment.irregularlysampledsignals[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
    #     print (path + "->spiketrains")
        for ivar_idx in range(len(segment1.spiketrains)):
            data[str(path+str("->spiketrains[" + str(ivar_idx) + "]") + "->")] = segment.spiketrains[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
        for ivar_idx in range(len(segment1.events)):
            data[str(path+str("->events[" + str(ivar_idx) + "]") + "->")] = segment.events[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
        for ivar_idx in range(len(segment1.epochs)):
            data[str(path+str("->epochs[" + str(ivar_idx) + "]") + "->")] = segment.epochs[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

# def compare_segments (segment1, segment2, path, all_failures, nb_errors, nb_values_total):
#     # if type(segment1) == type(None) or type(segment1) == type(None):
#     #     print ("Error NoneType ")
#
#     try:
#         # Group objects
#         print (path + "->channelview")
#         # print (segment1.channelview)
#         for ivar_idx in range(len(segment1.channelview)):
#             if segment1.channelview[ivar_idx].all() != segment2.channelview[ivar_idx].all():
#                 all_failures[str(path+str("->channelview[" + str(ivar_idx) + "]") + "->")] = segment1.channelview[ivar_idx] - segment2.channelview[ivar_idx]
#     except Exception as e:
#         print (type(segment1.channelview))
#         print (type(segment1))
#         print ("Error Neo :: " + str(e))
#
#     try:
#         print (path + "->analogsignals")
#         for ivar_idx in range(len(segment1.analogsignals)):
#             if segment1.analogsignals[ivar_idx].all() != segment2.analogsignals[ivar_idx].all():
#                 all_failures[str(path+str("->analogsignals[" + str(ivar_idx) + "]") + "->")] = segment1.analogsignals[ivar_idx] - segment2.analogsignals[ivar_idx]
#     except Exception as e:
#         print ("Error Neo :: " + str(e))
#
#     try:
#         print (path + "->irregularlysampledsignals")
#         for ivar_idx in range(len(segment1.irregularlysampledsignals)):
#             if segment1.irregularlysampledsignals[ivar_idx].all() != segment2.irregularlysampledsignals[ivar_idx].all():
#                 all_failures[str(path+str("->irregularlysampledsignals[" + str(ivar_idx) + "]") + "->")] = segment1.irregularlysampledsignals[ivar_idx] - segment2.irregularlysampledsignals[ivar_idx]
#     except Exception as e:
#         print ("Error Neo :: " + str(e))
#
#     try:
#         print (path + "->spiketrains")
#         for ivar_idx in range(len(segment1.spiketrains)):
#             print (segment1.spiketrains[ivar_idx])
#             if segment1.spiketrains[ivar_idx].all() != segment2.spiketrains[ivar_idx].all():
#                 all_failures[str(path+str("->spiketrains[" + str(ivar_idx) + "]") + "->")] = segment1.spiketrains[ivar_idx] - segment2.spiketrains[ivar_idx]
#     except Exception as e:
#         print ("Error Neo :: " + str(e))
#
#     try:
#         print (path + "->events")
#         for ivar_idx in range(len(segment1.events)):
#             if segment1.events[ivar_idx].all() != segment2.events[ivar_idx].all():
#                 all_failures[str(path+str("->events[" + str(ivar_idx) + "]") + "->")] = segment1.events[ivar_idx] - segment2.events[ivar_idx]
#     except Exception as e:
#         print ("Error Neo :: " + str(e))
#
#     try:
#         print (path + "->epochs")
#         for ivar_idx in range(len(segment1.epochs)):
#             if segment1.epochs[ivar_idx].all() != segment2.epochs[ivar_idx].all():
#                 all_failures[str(path+str("->epochs[" + str(ivar_idx) + "]") + "->")] = segment1.epochs[ivar_idx] - segment2.epochs[ivar_idx]
#     except Exception as e:
#         print ("Error Neo :: " + str(e))


# def compare_groups (group1, group2, path, all_failures, nb_errors, nb_values_total):
#     assert (len(group1.groups) == len (group2.groups))
#
#     for igroup_idx in range(len(group1.groups)):
#         compare_groups (group1.groups[igroup_idx], group2.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]")
#
#     compare_segments (group1, group2, path, all_failures, nb_errors, nb_values_total)

# def compare_neo_blocks (neoblock1, neoblock2, path, all_failures, nb_errors, nb_values_total):
#
#     assert(len(neoblock1.segments) == len(neoblock2.segments))
#     print ("nombre de segment = " + str(len(neoblock1.segments)))
#     for isegment_idx in range(len(neoblock1.segments)):
#         compare_segments (neoblock1.segments[isegment_idx], neoblock2.segments[isegment_idx], path + "->segment[" + str(isegment_idx) + "]", all_failures, nb_errors, nb_values_total)
#
#     print ("groups")
#
#     assert(len(neoblock1.groups) == len(neoblock2.groups))
#     print ("nombre de groupes = " + str(len(neoblock1.groups)))
#     for igroup_idx in range(len(neoblock1.groups)):
#         compare_groups (neoblock1.groups[igroup_idx], neoblock2.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]")

def compute_differences_report (file1, file2, path, all_failures, nb_errors, nb_values_total):
    try:
        file_path1 = self.file1.url + self.file1.name
        file_path2 = self.file2.url + self.file2.name

        neo_reader1 = neo.io.get_io(self.file1.url + self.file1.name)
        neo_reader2 = neo.io.get_io(self.file2.url + self.file2.name)

        blocks1 = neo_reader1.read()
        blocks2 = neo_reader2.read()

        # Assert blocks have same size
        if len(blocks1) != len(blocks2):
            print ("NEO Error:" + file_path1 + " and " + file_path2 + " do not have the same number of neo:blocks")
            print ("NEO Warning: Number of blocks are not equal: not all blocks will be compared" )

        print ("nombre de blocks = " + str(len(blocks1)))
        for iblock_idx in range(min(len(blocks1), len(blocks2))):
            compare_neo_blocks(blocks1[iblock_idx], blocks2[iblock_idx], "R->block[" + str(iblock_idx) + "]")
    except Exception as e:
        print ("Neo :: " + str(type(e).__name__) + " " + str(e))
