# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

def compute_differences_report (file1, file2):
    pass

def compute_score (number_of_errors, number_of_values):
    pass

def check_file_formats (filepath):
    try:
        fp = open(filepath, "b")
        return True, None
    except Exception as e:
        return False, str(e)


def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

def nilsimsa_files (f1_path, f2_path, buffer_size=32):
    with open(f1_path, "r") as f1:
        with open(f2_path, "r") as f2:
            linesf1 = f1.readlines()
            linesf2 = f2.readlines()
            assert(len(linesf1) == len(linesf2))
            for idx in range(len(linesf1)):

                # Set default filename
                filename1 = linesf1[idx].split("\n")[0]
                filename2 = linesf2[idx].split("\n")[0]

                nilsimsa_single(filename1, filename2, buffer_size)

def nilsimsa_single (f1_path, f2_path, buffer_size=32):

    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read(buffer_size)
        f2_byte = f2.read(buffer_size)

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
            f1_byte = f1.read(buffer_size)
            f2_byte = f2.read(buffer_size)


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
