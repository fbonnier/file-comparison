
# Fuzzy String comparisons
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def levenshtein (f1_path, f2_path, buffer_size=32):

    # Total Score
    TOTAL_SCORE = 0
    # Number of buffer used
    NBUFFER = 0

    # Open files in byte mode
    # Cut the files into N bytes with N=32
    # Compatible with Python 2.6 and Python 3.x
    # ref: https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read(buffer_size)
        f2_byte = f2.read(buffer_size)

        while f1_byte and f2_byte:
            # Run Levenshtein Distance computation
            score = fuzz.ratio(str(f1_byte), str(f2_byte))

            NBUFFER += 1
            TOTAL_SCORE += score
            # Initialize strings

            f1_byte = f1.read(buffer_size)
            f2_byte = f2.read(buffer_size)

        # Last comparison in case the files closed before filling 64 bytes arrays
        if len(str(f1_byte)):
            score = fuzz.ratio(str(f1_byte), str(f2_byte))
            NBUFFER += 1
            TOTAL_SCORE += score
            # print ("Last score for arrays of size " + str(len(f1_str)) + " " + str(len(f2_str)) + " = " + str(score))
        print ("Total = " + str(TOTAL_SCORE))
        print ("Total buffer = " + str(NBUFFER))
        print ("Total ratio = " + str(TOTAL_SCORE / NBUFFER) + " %")
