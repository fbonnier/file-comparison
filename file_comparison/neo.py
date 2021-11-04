# Neo
from collections.abc import Iterable
import neo.io


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

def compare_neo_blocks (neoblock1, neoblock2):
    all_segs1 = []
    for isegment in neoblock1.segments:
        all_segs1.append([sig for sig in isegment.analogsignals])
        all_segs1.append([sig for sig in isegment.spiketrains])
        all_segs1.append([sig for sig in isegment.events])
        all_segs1.append([sig for sig in isegment.epochs])
        all_segs1.append([sig for sig in isegment.irregularlysampledsignals])
        # print (isegment)

def read_neo_block (neoblock):
    for isegment in neoblock.segments:
        print (isegment)

def compare_neo_file (filename1, filename2):
    try:
        neo_reader1 = neo.io.get_io(filename1)
        neo_reader2 = neo.io.get_io(filename2)
        blocks1 = neo_reader1.read()
        blocks2 = neo_reader2.read()
        print ("nombre de blocks = " + str(len(blocks1)))
        for iblock in blocks1:
            read_neo_block(iblock)
    except Exception as e:
        print ("Neo.IO Error")
        print (e)

def read_neo_file (filename):
    try:
        neo_reader = neo.io.get_io(filename)
        blocks = neo_reader.read()
        print ("nombre de blocks = " + str(len(blocks)))
        for iblock in blocks:
            read_neo_block(iblock)
    except Exception as e:
        print ("Neo.IO Error")
        print (e)


def npz_values (f1_path, f2_path):
    with open(f1_path, "r") as f1:
        with open(f2_path, "r") as f2:
            linesf1 = f1.readlines()
            linesf2 = f2.readlines()
            assert(len(linesf1) == len(linesf2))
            for idx in range(len(linesf1)):

                # Set default filename
                filename1 = linesf1[idx].split("\n")[0]
                filename2 = linesf2[idx].split("\n")[0]

                npz_single(filename1, filename2, buffer_size)

def npz_single (f1_path, f2_path):

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

    ratio =  compute_ratio()
    print ("Ratio = " + str(ratio) + " %")
