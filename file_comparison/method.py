# Method class
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt

import file_comparison.neo
import file_comparison.npz
import file_comparison.file_compare
import file_comparison.nilsimsa


class Method:

    __name__ = ""
    __difference_methods__ = {"neo": file_comparison.neo.compute_differences_report, "npz": file_comparison.npz.compute_differences_report, "byte": file_comparison.nilsimsa.compute_differences_report}
    __score_methods__ = {"neo": file_comparison.neo.compute_score, "npz": file_comparison.npz.compute_score, "byte": file_comparison.nilsimsa.compute_score}
    __check_methods__ = {"neo": file_comparison.neo.check_file_formats, "npz": file_comparison.npz.check_file_formats, "byte": file_comparison.nilsimsa.check_file_formats}
    file1 = None
    file2 = None
    score = 0.
    differences_report = None
    number_of_errors = 0
    number_of_values = 0
    rmse_score = 0.
    mse_score = 0.
    mape_score = 0.

    # 1
    def __init__ (self, name, file_info_1, file_info_2):
        # TODO: Replace assert by Exception
        assert name in self.__difference_methods__, "Method \"" + name + "\" unsupported. Method should be \"npz\", \"neo\" or \"byte\""
        self.__name__ = name
        self.file1 = file_info_1
        self.file2 = file_info_2

    # 2
    def check_file_formats (self):
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
