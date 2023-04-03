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
    ipair = None
    score = 0.
    differences_report = None
    number_of_errors = 0
    number_of_values = 0
    rmse_score = 0.
    mse_score = 0.
    mape_score = 0.

    # 1.1
    def __init__ (self, ipair: dict):

        self.__name__ = ipair["method"]
        # TODO: Replace assert by Exception
        assert self.__name__ in self.__difference_methods__, "Method \"" + self.__name__ + "\" unsupported. Method should be \"npz\", \"neo\" or \"byte\""
        self.ipair = ipair

    # 2
    def check_file_formats (self):
        
        if self.ipair:
            self.check_file_formats_pair()
        
        else:
            try:
                return self.__check_methods__[self.__name__](self.file1, self.file2), {}
            except Exception as e:
                self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
                return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)

    # 2.pair
    def check_file_formats_pair (self):
        try:
            return self.__check_methods__[self.__name__](self.file1, self.file2), {}
        except Exception as e:
            self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
            return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)

    # 4
    def compute_score (self):
        try:
            self.score = self.__score_methods__[self.__name__](self.number_of_errors, self.number_of_values)
            self.mape_score = self.mape()
        except Exception as e:
            print (e)
        return self.score

    # 3
    def compute_differences_report (self):
        if self.ipair:
            try:
                # TODO
                self.differences_report, self.number_of_errors, self.number_of_values = self.__difference_methods__[self.__name__](self.ipair)
            except Exception as e:
                self.ipair["log"].append (e)
                self.ipair["error"].append (e)


        else:
            # TODO catch exception and report instead of assert
            assert self.file1 != None, "No file specified"
            assert self.file2 != None, "No file specified"

            try:
                self.differences_report, self.number_of_errors, self.number_of_values = self.__difference_methods__[self.__name__](self.file1, self.file2)
            except Exception as e:
                print (e)

        # except Exception as e:
        #     self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
        #     return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)

    def topair (self, ipair):
        ipair["method"] = self.__name__
        ipair["score"] = self.score
        ipair["rmse"] = self.rmse_score
        ipair["mape"] = self.mape_score
        ipair["mse"] = self.mse_score
        ipair["differences"] = self.differences_report
        # ipair["mse"] = self.mse_score
        # ipair["mse"] = self.mse_score
        # ipair["mse"] = self.mse_score

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
    
    # Guessing the file type based on its extension
    # NPZ
    try:
        data1 = numpy.load(ipair["File1"]["path"])
        data2 = numpy.load(ipair["File2"]["path"])

        ipair["method"] = "npz"

    except Exception as enumpy:

        # NEO
        try:
            neo_reader1 = neo.io.get_io(ipair["File1"]["path"])
            neo_reader2 = neo.io.get_io(ipair["File2"]["path"])
            ipair["method"] =  "neo"

        except Exception as eneo:
            ipair["method"] = "byte"

    return ipair