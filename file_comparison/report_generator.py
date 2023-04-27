# Report generator Module
import os
import file_comparison.file_compare as file_compare
from nltk.metrics.distance import *
import sklearn.metrics

error_diff_types = ["type", "len"]


def compute_1el_difference (origin, new):

    return compute_1list_difference ([origin], [new])


def compute_1list_difference (origin, new):
    block_diff_1list = {"origin": {"type": str(type(origin)), "value": origin}, "new": {"type": str(type(new)), "value": new}, "nilsimsa": None, "rmspe": None, "mspe": None, "mape": None, "error": [], "log": []}

    # Test types: if types are different, return error type
    if type(origin) != type(new):
        block_diff_1list["error"] = "Values are not the same type"
        return (block_diff_1list)

    # # Test delta
    # # Compute Absolute difference between two values
    # try:
    #     block_diff_1list["delta"] = abs(origin - new)
    # except:
    #     pass

    # Test string values
    # Compute Levenshtein distance between two strings
    try:
        block_diff_1list["levenshtein"] = nltk.metrics.distance.edit_distance(origin, new)
    except:
        pass


    # Test mape
    # Compute Absolute Percentage Error between two values
    try:
        block_diff_1list["mape"] = sklearn.metrics.mean_absolute_percentage_error(origin, new)
    except:
        pass
    
    # Test mspe
    # Compute Mean Squared Percentage Error between two values
    try:
        block_diff_1list["mspe"] = mean_squared_percentage_error(origin, new)
    except:
        pass

    # Test rmspe
    # Compute Root Mean Squared Percentage Error between two lists
    try:
        block_diff_1list["mspe"] = root_mean_squared_percentage_error(origin, new)
    except:
        pass

    return block_diff_1list
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
