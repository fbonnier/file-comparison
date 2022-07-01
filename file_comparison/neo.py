# Neo
from collections.abc import Iterable
import neo.io

all_failures = {}


def compute_ratio ():
    print ("Number of errors = " + str (nb_errors))
    print ("Number of values = " + str (nb_values_total))
    print ("Number of failures = " + str (len(all_failures)) + "\n")

    for ifail in all_failures:
        print (type(ifail))
        print (ifail)
        print (type(all_failures[ifail]))
        print (all_failures[ifail])
        print ("\n")

    return (100. - (nb_errors*100./nb_values_total))


def compare_segments (segment1, segment2, path):
    # if type(segment1) == type(None) or type(segment1) == type(None):
    #     print ("Error NoneType ")

    try:
        # Group objects
        print (path + "->channelview")
        # print (segment1.channelview)
        for ivar_idx in range(len(segment1.channelview)):
            if segment1.channelview[ivar_idx].all() != segment2.channelview[ivar_idx].all():
                all_failures[str(path+str("->channelview[" + str(ivar_idx) + "]") + "->")] = segment1.channelview[ivar_idx] - segment2.channelview[ivar_idx]
    except Exception as e:
        print (type(segment1.channelview))
        print (type(segment1))
        print ("Error Neo :: " + str(e))

    try:
        print (path + "->analogsignals")
        for ivar_idx in range(len(segment1.analogsignals)):
            if segment1.analogsignals[ivar_idx].all() != segment2.analogsignals[ivar_idx].all():
                all_failures[str(path+str("->analogsignals[" + str(ivar_idx) + "]") + "->")] = segment1.analogsignals[ivar_idx] - segment2.analogsignals[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
        print (path + "->irregularlysampledsignals")
        for ivar_idx in range(len(segment1.irregularlysampledsignals)):
            if segment1.irregularlysampledsignals[ivar_idx].all() != segment2.irregularlysampledsignals[ivar_idx].all():
                all_failures[str(path+str("->irregularlysampledsignals[" + str(ivar_idx) + "]") + "->")] = segment1.irregularlysampledsignals[ivar_idx] - segment2.irregularlysampledsignals[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
        print (path + "->spiketrains")
        for ivar_idx in range(len(segment1.spiketrains)):
            print (segment1.spiketrains[ivar_idx])
            if segment1.spiketrains[ivar_idx].all() != segment2.spiketrains[ivar_idx].all():
                all_failures[str(path+str("->spiketrains[" + str(ivar_idx) + "]") + "->")] = segment1.spiketrains[ivar_idx] - segment2.spiketrains[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
        print (path + "->events")
        for ivar_idx in range(len(segment1.events)):
            if segment1.events[ivar_idx].all() != segment2.events[ivar_idx].all():
                all_failures[str(path+str("->events[" + str(ivar_idx) + "]") + "->")] = segment1.events[ivar_idx] - segment2.events[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
        print (path + "->epochs")
        for ivar_idx in range(len(segment1.epochs)):
            if segment1.epochs[ivar_idx].all() != segment2.epochs[ivar_idx].all():
                all_failures[str(path+str("->epochs[" + str(ivar_idx) + "]") + "->")] = segment1.epochs[ivar_idx] - segment2.epochs[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

def compare_groups (group1, group2, path):
    assert (len(group1.groups) == len (group2.groups))

    for igroup_idx in range(len(group1.groups)):
        compare_groups (group1.groups[igroup_idx], group2.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]")

    compare_segments (group1, group2, path)

def compare_neo_blocks (neoblock1, neoblock2, path):

    assert(len(neoblock1.segments) == len(neoblock2.segments))
    print ("nombre de segment = " + str(len(neoblock1.segments)))
    for isegment_idx in range(len(neoblock1.segments)):
        compare_segments (neoblock1.segments[isegment_idx], neoblock2.segments[isegment_idx], path + "->segment[" + str(isegment_idx) + "]")

    print ("groups")

    assert(len(neoblock1.groups) == len(neoblock2.groups))
    print ("nombre de groupes = " + str(len(neoblock1.groups)))
    for igroup_idx in range(len(neoblock1.groups)):
        compare_groups (neoblock1.groups[igroup_idx], neoblock2.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]")

def compare_neo_file (filename1, filename2):
    try:
        neo_reader1 = neo.io.get_io(filename1)
        neo_reader2 = neo.io.get_io(filename2)

        blocks1 = neo_reader1.read()
        blocks2 = neo_reader2.read()
        # Assert blocks have same size
        if len(blocks1) != len(blocks2):
            print ("NEO Error:" + filename1 + " and " + filename2 + " do not have the same number of neo:blocks")
            "R->block[" + str(iblock_idx) + "]"


        print ("nombre de blocks = " + str(len(blocks1)))
        for iblock_idx in range(len(blocks1)):
            compare_neo_blocks(blocks1[iblock_idx], blocks2[iblock_idx], "R->block[" + str(iblock_idx) + "]")
    except Exception as e:
        print ("Neo :: " + str(type(e).__name__) + " " + str(e))
