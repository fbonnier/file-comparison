# Report generator Module
import os
import file_comparison.file_compare as file_compare
from nltk.metrics.distance import *

error_diff_types = ["type", "len"]


def compute_1el_difference (item1, item2):
    block_diff_1el = {"type1": str(type(item1)), "value1": item1, "type2": str(type(item1)), "value2": item2, "delta": None, "levenshtein": None, "rmse": None, "mse": None, "ape": None, "error": [], "log": []}
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



    # Test ape
    # Compute Absolute Percentage Error between two values
    try:
        block_diff_1el["ape"] = abs((item1-item2)/item1)
    except:
        pass

    return block_diff_1el


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
