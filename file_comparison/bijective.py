# List of comparison methods to compare two files and retrieve closest ones

# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests

# Magic - determine file formats of outputs
import magic

# Determine if file1 and file2 are the same format
#   file1, file2: {"url", "path", "hash"}
def are_same_file_format (file1, file2):
    file1_format = magic.from_file(file1["path"], mime = True)
    file2_format = magic.from_file(file2["path"], mime = True)

    block = {"format": [],"format score": None, "format error": None}
    if file1_format == file2_format:
        block["format score"] = True
        block["format"].append (file1_format)
    else:
        block["format score"] = False
        block["format"].append (file1_format)
        block["format"].append (file2_format)
        block["format error"] = "Error: " + file1["path"] + " is " + str(file1_format) + " | " + file2["path"] + " is " + str(file2_format)

    return block

def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

def find_bijective (list_of_file1, list_of_file2):

    # Walk the files and build blocks of pairs
    blocks_of_pairs = [] 
    for ifile1 in list_of_file1:
        partner = {"ifile2": None, "score": 0}
        # Search for nearest partner
        for ifile2 in list_of_file2:
            new_score = compute_ratio(compare_digests(Nilsimsa(ifile1["filename"] + str(ifile1["size"])).hexdigest(), Nilsimsa(ifile2["filename"] + str(ifile2["size"])).hexdigest()))
            # new_score = compute_ratio(compare_digests(hex(ifile1["hash"]), hex(ifile2["hash"])))
            # new_score = 0.1
            if partner["score"] < new_score:
                partner["ifile2"] = ifile2
                partner["score"] = new_score
        block = {"File1": None, "File2": None, "hash score": None, "format": None, "error": [], "method": None}
        block["File1"] = ifile1
        block["File2"] = partner["ifile2"]
        block["hash score"] = partner["score"]

        # # Compare file formats
        # format_block = are_same_file_format (ifile1, partner["ifile2"])
        # if format_block["format score"]:
        #     block["format"] = format_block["format"][0]
        # else:
        #     block["format"] = format_block["format"]
        #     block["error"].append(format_block["error"])

        blocks_of_pairs.append(block)

    return blocks_of_pairs