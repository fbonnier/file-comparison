# Method class
import numpy
import neo

from sklearn.metrics import mean_squared_error
from math import sqrt

import file_comparison.neo
import file_comparison.npz
import file_comparison.nilsimsa


class Method:

    __name__ = ""
    __difference_methods__ = {"neo": file_comparison.neo.compute_differences_report, "npz": file_comparison.npz.compute_differences_report, "byte": file_comparison.nilsimsa.compute_differences_report}
    __score_methods__ = {"neo": file_comparison.neo.compute_score, "npz": file_comparison.npz.compute_score, "byte": file_comparison.nilsimsa.compute_score}
    __check_methods__ = {"neo": file_comparison.neo.check_file_formats, "npz": file_comparison.npz.check_file_formats, "byte": file_comparison.nilsimsa.check_file_formats}
    file1 = None
    file2 = None
    score = 0.
    quantity_score = 0.
    differences_report = None
    mean_value = 0.
    number_of_errors = 0
    number_of_values = 0
    rmse_score = 0.
    mse_score = 0.
    mape_score = 0.
    errors = []
    log = []

    # 1.1
    def __init__ (self, ipair: dict):

        self.__name__ = ipair["method"]
        # TODO: Replace assert by Exception
        assert self.__name__ in self.__difference_methods__, "Method \"" + self.__name__ + "\" unsupported. Method should be \"npz\", \"neo\" or \"byte\""
        self.file1 = ipair["File1"]
        self.file2 = ipair["File2"]

    # 2
    def check_file_formats (self):
        check1 = False
        check2 = False
        error1 = None
        error2 = None

        if not (self.file1 or self.file2):
            return False, "Method.check_file_formats: Unknown files"
        else:
            try:
                check1, error1 = self.__check_methods__[self.__name__](self.file1["path"])
            except Exception as e:
                check1 = False
                error1 = "Method.check_file_formats: " + e
            try:
                check2, error2 = self.__check_methods__[self.__name__](self.file2["path"])
            except Exception as e:
                check2 = False
                error2 = "Method.check_file_formats: " + e
                # self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
                # return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)
        check = check1 and check2
        error = [error1,  error2] if error1 and error2 else None
        return check, error 

    # 2.pair
    def check_file_formats_pair (self):
        try:
            return self.__check_methods__[self.__name__](self.file1, self.file2), {}
        except Exception as e:
            self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
            return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)

    # 4
    def compute_score (self):

        # Calculate the ratio of different values compared to total number of values
        self.quantity_score = 100. - self.number_of_errors*100./self.number_of_values

        # Calculate MAPE
        apes = [ipair["ape"] for ipair in self.differences_report if self.differences_report[ipair]["ape"]]
        # apes = []
        # for ipair in self.differences_report:
        #     print (ipair)
        #     print ("\n")
            # if ipair["ape"]:
            #     apes.append(ipair["ape"])

        if apes:
            self.mape_score = 100. - (sum(apes)/len(apes) * 100.)

        # # Calculate Mean Error
        # deltas = [ipair["delta"] for ipair in self.differences_report if ipair["delta"]]
        # if deltas:
        #     self.mean_error = sum(deltas)/len(deltas)
            
        # # Calculate MSE
        # # TODO

        # # Calculate RMSE
        # # TODO

        # # try:
        # #     self.score = self.__score_methods__[self.__name__](self.number_of_errors, self.number_of_values)
        # # except Exception as e:
        # #     print (e)
        # # return self.score

    # 3
    def compute_differences (self):
        if not (self.file1 or self.file2):
            self.errors.append("Method.compute_differences: Unknown files")
        
        try:
            # TODO
            block_diff = self.__difference_methods__[self.__name__](self.file1, self.file2)
            self.differences_report = block_diff["report"]
            self.number_of_errors = block_diff["nerrors"]
            self.number_of_values = block_diff["nvalues"]
            self.log = block_diff["log"]
            self.errors += block_diff["error"]
            
        except Exception as e:
            self.log.append ("Method.compute_differences: " + str(e))
            self.errors.append ("Method.compute_differences: " + str(e))

    def topair (self, ipair):
        ipair["method"] = self.__name__
        ipair["error"] = self.errors
        ipair["log"] = self.log
        ipair["score"] = self.score
        ipair["differences"] = self.differences_report
        ipair["number_of_errors"] = self.number_of_errors
        ipair["number_of_values"] = self.number_of_values
        ipair["rmse_score"] = self.rmse_score
        ipair["mse_score"] = self.mse_score
        ipair["mape_score"] = self.mape_score
        ipair["quantity score"] = self.quantity_score
        
        return ipair

# class Method:

#     __name__ = ""
#     __difference_methods__ = {"neo": file_comparison.neo.compute_differences_report, "npz": file_comparison.npz.compute_differences_report, "byte": file_comparison.nilsimsa.compute_differences_report}
#     __score_methods__ = {"neo": file_comparison.neo.compute_score, "npz": file_comparison.npz.compute_score, "byte": file_comparison.nilsimsa.compute_score}
#     __check_methods__ = {"neo": file_comparison.neo.check_file_formats, "npz": file_comparison.npz.check_file_formats, "byte": file_comparison.nilsimsa.check_file_formats}
#     file1 = None
#     file2 = None
#     ipair = None
#     score = 0.
#     differences_report = None
#     number_of_errors = 0
#     number_of_values = 0
#     rmse_score = 0.
#     mse_score = 0.
#     mape_score = 0.

#     # 1.1
#     def __init__ (self, name, file_info_1, file_info_2):
#         # TODO: Replace assert by Exception
#         assert name in self.__difference_methods__, "Method \"" + name + "\" unsupported. Method should be \"npz\", \"neo\" or \"byte\""
#         self.__name__ = name
#         self.file1 = file_info_1
#         self.file2 = file_info_2

#     # 1.pair
#     def __init__ (self, ipair: dict):
#         # TODO: Replace assert by Exception
#         assert ipair["method"] in self.__difference_methods__, "Method \"" + name + "\" unsupported. Method should be \"npz\", \"neo\" or \"byte\""
#         self.__name__ = name
#         self.ipair = ipair

#     # 2
#     def check_file_formats (self):
        
#         if self.ipair:
#             self.check_file_formats_pair()
        
#         else:
#             try:
#                 return self.__check_methods__[self.__name__](self.file1, self.file2), {}
#             except Exception as e:
#                 self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
#                 return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)

#     # 2.pair
#     def check_file_formats_pair (self):
#         try:
#             return self.__check_methods__[self.__name__](self.file1, self.file2), {}
#         except Exception as e:
#             self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
#             return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)

#     # 4
#     def compute_score (self):
#         try:
#             self.score = self.__score_methods__[self.__name__](self.number_of_errors, self.number_of_values)
#             self.mape_score = self.mape()
#         except Exception as e:
#             print (e)
#         return self.score

#     # 3
#     def compute_differences_report (self):
#         # TODO catch exception and report instead of assert
#         assert self.file1 != None, "No file specified"
#         assert self.file2 != None, "No file specified"

#         try:
#             self.differences_report, self.number_of_errors, self.number_of_values = self.__difference_methods__[self.__name__](self.file1, self.file2)
#         except Exception as e:
#             print (e)

#         # except Exception as e:
#         #     self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
#         #     return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)

#     def topair (self, ipair):
#         ipair["method"] = self.__name__
#         ipair["score"] = self.score
#         ipair["rmse"] = self.rmse_score
#         ipair["mape"] = self.mape_score
#         ipair["mse"] = self.mse_score
#         ipair["differences"] = self.differences_report
#         # ipair["mse"] = self.mse_score
#         # ipair["mse"] = self.mse_score
#         # ipair["mse"] = self.mse_score

#         return ipair

def get_adviced_method (ipair):
    
    # Guessing the file
    
    ########## NUMPY ##########
    # allow_pickle, bytes encoded
    try:
        data1 = numpy.load(ipair["File1"]["path"], allow_pickle=True, encoding='bytes')
        data2 = numpy.load(ipair["File2"]["path"], allow_pickle=True, encoding='bytes')

        ipair["method"] = "npz"
        ipair["File1"]["encoding"] = "bytes"
        ipair["File2"]["encoding"] = "bytes"
        ipair["File1"]["allow_pickle"] = True
        ipair["File2"]["allow_pickle"] = True
        return ipair
    except Exception as e:
        pass

    # allow_pickle, ascii encoded
    try:
        data1 = numpy.load(ipair["File1"]["path"], allow_pickle=True, encoding='ASCII')
        data2 = numpy.load(ipair["File2"]["path"], allow_pickle=True, encoding='ASCII')

        ipair["method"] = "npz"
        ipair["File1"]["encoding"] = "ASCII"
        ipair["File2"]["encoding"] = "ASCII"
        ipair["File1"]["allow_pickle"] = True
        ipair["File2"]["allow_pickle"] = True
        return ipair
    except Exception as e:
        pass

        ########## NEO ##########
    try:
        neo_reader1 = neo.io.get_io(ipair["File1"]["path"])
        neo_reader2 = neo.io.get_io(ipair["File2"]["path"])
        ipair["method"] =  "neo"
        ipair["File1"]["encoding"] = None
        ipair["File2"]["encoding"] = None
        ipair["File1"]["allow_pickle"] = None
        ipair["File2"]["allow_pickle"] = None
        return ipair

    except Exception as eneo:
        pass

    ########## BYTES ##########
    ipair["method"] = "byte"
    ipair["File1"]["encoding"] = None
    ipair["File2"]["encoding"] = None
    ipair["File1"]["allow_pickle"] = None
    ipair["File2"]["allow_pickle"] = None

    return ipair