# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

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
