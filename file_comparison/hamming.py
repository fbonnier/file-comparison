# Hamming
from scipy.spatial.distance import hamming

## Computes Hamming Distance between seq1 and seq2
#  Using Scipy spatial distance
def hamming_distance_scipy (seq1, seq2):
    return hamming(seq1, seq2) * len(seq1)

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
            # score = hamming_distance(f1_byte, f2_byte)
            score = hamming_distance_scipy(f1_byte, f2_byte)

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
