# Report generator Module
import os
# import file_comparison.file_compare as file_compare
import file_comparison.stats as stats
import numpy as np

error_diff_types = ["type", "len"]


def compute_1el_difference (origin, new):

    print ("Report_generator: compute_1el_difference")
    return compute_1list_difference (np.asarray(origin), np.asarray(new))


def compute_1list_difference (origin:np.ndarray, new:np.ndarray):
 
    block_diff_1list = {"origin": {"type": str(type(origin.tolist())), "value": origin.tolist()}, "new": {"type": str(type(new.tolist())), "value": new.tolist()}, "levenshtein": None, "nilsimsa": None, "rmspe": None, "mspe": None, "mape": None, "mpe":None, "rpd": None , "error": [], "log": []}

    print ("Report_generator: compute_1list_difference")


    # # Test types: if types are different, return error type
    # if type(origin) != type(new):
    #     block_diff_1list["error"] = "Values are not the same type"
    #     return (block_diff_1list)

    # # Test delta
    # # Compute Absolute difference between two values
    # try:
    #     block_diff_1list["delta"] = abs(origin - new)
    # except:
    #     pass

    # Test string values
    # Compute Levenshtein distance percentage between two strings
    # TODO
    try:
        block_diff_1list["levenshtein"] = stats.mean_levenshtein_distance_percentage(origin, new)
    except Exception as e:
        print ("Levenshtein Stat")
        print (e)


    # Test mape
    # Compute Absolute Percentage Error between two values
    try:
        block_diff_1list["mape"] = stats.mean_absolute_percentage_error(origin, new)
    except Exception as e:
        print ("MAPE Stat")
        block_diff_1list["log"].append(e)
        block_diff_1list["mape"] = None
        print (e)
    
    # Test mspe
    # Compute Mean Squared Percentage Error between two values
    # TODO
    try:
        block_diff_1list["mspe"] = stats.mean_squared_percentage_error(origin, new)        
    except Exception as e:
        print ("MSPE Stat")
        print (e)
        block_diff_1list["log"].append(e)
        block_diff_1list["mspe"] = None

    # Test rmspe
    # Compute Root Mean Squared Percentage Error between two lists
    try:
        block_diff_1list["rmspe"] = stats.root_mean_squared_percentage_error(origin, new)        
    except Exception as e:
        block_diff_1list["log"].append(e)
        block_diff_1list["rmspe"] = None
        print ("RMSPE Stat")
        print (e)

    # Test mpe
    # Compute Mean Percentage Error between two lists
    try:
        block_diff_1list["mpe"] = stats.mean_percentage_error(origin, new)
        print ("MPE = " + str(block_diff_1list["mpe"]))
    except Exception as e:
        print ("MPE Stat")
        block_diff_1list["log"].append(e)
        block_diff_1list["mpe"] = None
        print (e)
    
    # Test rpd
    # Compute Relative Percentage Difference between two lists
    # TODO
    try:
        block_diff_1list["rpd"] = stats.mean_relative_percentage_difference(origin, new)
        print ("RPD = " + str(block_diff_1list["rpd"]))
    except Exception as e:
        print ("RPD Stat")
        block_diff_1list["log"].append(e)
        block_diff_1list["rpd"] = None
        print (e)
    
    # Test nilsimsa
    # Compute Nilsimsa Distane between two lists
    # try:
        # block_diff_1list["nilsimsa"] = stats.root_mean_squared_percentage_error(origin, new)
    # except ZeroDivisionError as ed:        
        # block_diff_1list["log"].append(ed)
        # block_diff_1list["rpd"] = None
    # except Exception as e:
    #     print (e)
    #     print ("Origin: ")
    #     print (origin)
    #     print ("\n")
    #     print ("New: ")
    #     print (new)


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

# def compute_differences (file1, file2, method):

#     ratio = 0.
#     differences = {}
#     try:
#         print (method)
#         print (file_compare.all_methods[method])
#         ratio, differences = file_compare.all_methods[method](file1.url+file1.name, file2.url+file2.name)
#         print ("SCORE = " + str(ratio))

#     except Exception as e:
#         print ("\nError: method " + method + " Exception for " + file1.name + " and " + file2.name)
#         print (e)
#         ratio = 0.
#         differences = {"error" : str(e)}

#     return ratio, differences
