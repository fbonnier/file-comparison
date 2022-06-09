# Report generator Module
import os
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

    # Block to return
    blck = {"file1":
                {
                    "name":os.path.basename(file1),
                    "path":os.path.dirname(file1),
                    "size":os.path.getsize(file1),
                    "type":os.path.splitext(file1)[1],
                },
            "file2":
                {
                    "name":os.path.basename(file2),
                    "path":os.path.dirname(file2),
                    "size":os.path.getsize(file2),
                    "type":os.path.splitext(file2)[1],
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
