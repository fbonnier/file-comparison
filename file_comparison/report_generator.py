# Report generator Module
import os
import file_comparison.file_compare as file_compare
from nltk.metrics.distance import *

error_diff_types = ["type", "len"]


def compute_1el_difference (item1, item2):
    block_diff_1el = {"type1": str(type(item1)), "value1": item1, "type2": str(type(item1)), "value2": item2, "delta": None, "levenshtein": None, "rmse": None, "mse": None, "ape": None, "error": None}
    # Test types: if types are different, return error type
    if type(item1) != type(item2):
        block_diff_1el["error"] = "Values are not the same type"
        return (block_diff_1el)

    # Test delta
    # Compute Absolute difference between two values
    try:
        block_diff_1el["delta"] = abs(item1 - item2)
    except:
        pass

    # Test string values
    # Compute Levenshtein distance between two strings
    try:
        block_diff_1el["levenshtein"] = nltk.metrics.distance.edit_distance(item1, item2)
    except:
        pass

    # # Test rmse
    # # Compute Root Mean Square Error between two values
    # try:
    #     block_diff_1el["rmse"] = nltk.metrics.distance.edit_distance(item1, item2)
    # except:
    #     pass

    # # Test mse
    # # Compute Mean Square Error between two values
    # try:
    #     block_diff_1el["mse"] = nltk.metrics.distance.edit_distance(item1, item2)
    # except:
    #     pass

    # Test mape
    # Compute Absolute Percentage Error between two values
    try:
        block_diff_1el["ape"] = abs((item1-item2)/item1)
    except:
        pass

    return block_diff_1el




# Generates the final report that compiles differences and scores of file comparison
# The output report is an array of file couples organized like the following
# {"file1":{
#       "name":"test-file.txt",
#       "path":"",
#       "size":"1000",
#       "type":"file",
#     },
#  "file2":{
#         "name":"test-file.txt",
#         "path":"",
#         "size":"1000",
#         "type":"file",},
#  "method":"",
#  "score":"",
#  "differences":{},
# },
# input:
#       - file1: file path
#       - file2: file path
#       - method: method used to compare the files (neo, numpy, bytes)
#       - score: score of the comparison
#       - differences: list of differences
def generate_report_1_file (file1, file2, method, score, differences):
    file1_path = file1.url + file1.name
    file2_path = file2.url + file2.name
    # Block to return
    blck = {"file1":
                {
                    "name":os.path.basename(file1_path),
                    "path":os.path.dirname(file1_path),
                    "size":os.path.getsize(file1_path),
                    "type":os.path.splitext(file1_path)[1],
                },
            "file2":
                {
                    "name":os.path.basename(file2_path),
                    "path":os.path.dirname(file2_path),
                    "size":os.path.getsize(file2_path),
                    "type":os.path.splitext(file2_path)[1],
                },
            "method":method,
            "score": score,
            "differences": differences
            }
    return blck

"""
Differences object should look like:
------------------
neo objects
{
    'block x':
    {
        'segment y':
        {
            'data array z':
            {
                'item i': abs (item m - item n)
            }
        }
    }
    'missing data':
    {
        'block x':
        {
            'segment y':
            {
                'data array z': [item m, item n, ...]
            }
        }
    }
}

-------------------
numpy objects
{
    'array x':
    {
        'item i': abs (item m - item n)
    }
}
-------------------
byte method objects
{
    'block x':
}
"""

def compute_differences (file1, file2, method):

    ratio = 0.
    differences = {}
    try:
        print (method)
        print (file_compare.all_methods[method])
        ratio, differences = file_compare.all_methods[method](file1.url+file1.name, file2.url+file2.name)
        print ("SCORE = " + str(ratio))

    except Exception as e:
        print ("\nError: method " + method + " Exception for " + file1.name + " and " + file2.name)
        print (e)
        ratio = 0.
        differences = {"error" : str(e)}

    return ratio, differences
