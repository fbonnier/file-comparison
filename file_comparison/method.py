# Method class
import numpy
import neo

from sklearn.metrics import mean_squared_error
from math import sqrt

import file_comparison.neo
import file_comparison.npz
# Nilsimsa
import file_comparison.nilsimsa
from nilsimsa import Nilsimsa, compare_digests


class Method:

    __name__ = ""
    __difference_methods__ = {"neo": file_comparison.neo.compute_differences_report, "npz": file_comparison.npz.compute_differences_report, "byte": file_comparison.nilsimsa.compute_differences_report}
    __score_methods__ = {"neo": file_comparison.neo.compute_score, "npz": file_comparison.npz.compute_score, "byte": file_comparison.nilsimsa.compute_score}
    __check_methods__ = {"neo": file_comparison.neo.check_file_formats, "npz": file_comparison.npz.check_file_formats, "byte": file_comparison.nilsimsa.check_file_formats}
    original_file = None
    new_file = None
    score = 0.
    quantity_score = 0.
    differences_report = []
    mean_value = 0.
    number_of_errors = 0
    number_of_values = 0
    rmse_score = 0.
    mse_score = 0.
    mape_score = 0.
    hash_score = 0.
    errors = []
    log = []

    # 1.1
    def __init__ (self, ipair: dict):

        self.__name__ = ipair["method"]
        # TODO: Replace assert by Exception
        assert self.__name__ in self.__difference_methods__, "Method \"" + self.__name__ + "\" unsupported. Method should be \"npz\", \"neo\" or \"byte\""
        self.original_file = ipair["Origin"]
        self.new_file = ipair["New"]

    # 2
    def check_file_formats (self):
        check1 = False
        check2 = False
        error1 = None
        error2 = None

        if not (self.original_file or self.new_file):
            return False, "Method.check_file_formats: Unknown files"
        else:
            try:
                check1, error1 = self.__check_methods__[self.__name__](self.original_file["path"])
            except Exception as e:
                check1 = False
                error1 = "Method.check_file_formats: " + e
            try:
                check2, error2 = self.__check_methods__[self.__name__](self.new_file["path"])
            except Exception as e:
                check2 = False
                error2 = "Method.check_file_formats: " + e
                # self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
                # return False, file_comparison.report_generator.generate_report_1_file (self.original_file, self.new_file, self.__name__, self.score, self.differences_report)
        check = check1 and check2
        error = [error1,  error2] if error1 and error2 else []
        return check, error 
    
    # Compare the two file's hash
    def compare_hash (self):
        try:
            with open(self.original_file, "rb") as foriginal, open(self.new_file, "rb") as fnew:
                original_hash = Nilsimsa (foriginal.read())
                new_hash = Nilsimsa (fnew.read())
                score_nilsimsa = compare_digests (original_hash.hexdigest(), new_hash.hexdigest())
                print(score_nilsimsa)
                ratio = file_comparison.nilsimsa.compute_ratio (score_nilsimsa)
                print(ratio)
                self.hash_score = ratio*100.
                print(self.hash_score)
        except Exception as e:
            self.number_of_errors += 1
            self.errors.append("compare_hash error: " + str(e))
            self.log.append("compare_hash error: " + str(e))

    # 2.pair
    def check_file_formats_pair (self):
        try:
            return self.__check_methods__[self.__name__](self.original_file, self.new_file), {}
        except Exception as e:
            self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
            return False, file_comparison.report_generator.generate_report_1_file (self.original_file, self.new_file, self.__name__, self.score, self.differences_report)

    # 4
    def compute_score (self):

        # Calculate the ratio of different values compared to total number of values
        self.quantity_score = 100. - self.number_of_errors*100./self.number_of_values

        # Calculate MAPE
        apes = [ipair["ape"] for ipair in self.differences_report if ipair["ape"]]
        # apes = []
        # for ipair in self.differences_report:
            # if ipair["ape"]:
                # apes.append(ipair["ape"])

        if apes:
            # self.mape_score = 100. - (sum(apes)/len(apes) * 100.)
            self.mape_score = 100. - (sum(apes)/self.number_of_values * 100.)

            
        # # Calculate MSE
        squared_deltas = [ipair["delta"]*ipair["delta"] for ipair in self.differences_report if ipair["delta"]]
        if squared_deltas:
            self.mse_score = sum(squared_deltas)/self.number_of_values

        # Calculate RMSE
        if self.mse_score:
            self.rmse_score = sqrt(self.mse_score)

        # # try:
        # #     self.score = self.__score_methods__[self.__name__](self.number_of_errors, self.number_of_values)
        # # except Exception as e:
        # #     print (e)
        # # return self.score

    # 3
    def compute_differences (self):
        if not (self.original_file or self.new_file):
            self.errors.append("Method.compute_differences: Unknown files")
        
        try:
            # TODO
            block_diff = self.__difference_methods__[self.__name__](self.original_file, self.new_file)
            # print (block_diff)
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
        ipair["hash score"] = self.hash_score
        
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
        data1 = numpy.load(ipair["Origin"]["path"], allow_pickle=True, encoding='bytes')
        data2 = numpy.load(ipair["New"]["path"], allow_pickle=True, encoding='bytes')

        ipair["method"] = "npz"
        ipair["Origin"]["encoding"] = "bytes"
        ipair["New"]["encoding"] = "bytes"
        ipair["Origin"]["allow_pickle"] = True
        ipair["New"]["allow_pickle"] = True
        return ipair
    except Exception as e:
        pass

    # allow_pickle, ascii encoded
    try:
        data1 = numpy.load(ipair["Origin"]["path"], allow_pickle=True, encoding='ASCII')
        data2 = numpy.load(ipair["New"]["path"], allow_pickle=True, encoding='ASCII')

        ipair["method"] = "npz"
        ipair["Origin"]["encoding"] = "ASCII"
        ipair["New"]["encoding"] = "ASCII"
        ipair["Origin"]["allow_pickle"] = True
        ipair["New"]["allow_pickle"] = True
        return ipair
    except Exception as e:
        pass

        ########## NEO ##########
    try:
        neo_reader1 = neo.io.get_io(ipair["Origin"]["path"])
        neo_reader2 = neo.io.get_io(ipair["New"]["path"])
        ipair["method"] =  "neo"
        ipair["Origin"]["encoding"] = None
        ipair["New"]["encoding"] = None
        ipair["Origin"]["allow_pickle"] = None
        ipair["New"]["allow_pickle"] = None
        return ipair

    except Exception as eneo:
        pass

    ########## BYTES ##########
    ipair["method"] = "byte"
    ipair["Origin"]["encoding"] = None
    ipair["New"]["encoding"] = None
    ipair["Origin"]["allow_pickle"] = None
    ipair["New"]["allow_pickle"] = None

    return ipair