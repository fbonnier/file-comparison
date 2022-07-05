# Method class
from file_comparison.file_compare import FileInfo
from file_comparison import *


class Method:

    __name__ = ""
    __difference_methods__ = {"neo": file_comparison.neo.compute_differences_report, "npz": file_comparison.npz., "byte": file_comparison.nilsimsa.}
    __score_methods__ = {"neo": file_comparison.neo.compute_score, "npz": file_comparison.npz.compute_score, "byte": file_comparison.nilsimsa.compute_score}
    __check_methods__ = {"neo": file_comparison.neo.check_array_size_warning, "npz": file_comparison.npz., "byte": file_comparison.nilsimsa.}
    file1 = None
    file2 = None
    score = 0.
    differences_report = []
    number_of_errors = 0
    number_of_values = 0

    def __init__ (self, name, file_info_1, file_info_2):
        assert (name in __difference_methods__)
        self.__name__ = name
        self.file1 = file_info_1
        self.file2 = file_info_2

    def check_file_formats (self):
        try:
            return self.__check_methods__[self.__name__](self.file1, self.file2), {}
        except Exception as e:
            self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
            return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)

    def compute_score (self):
        try:
            return self.__score_methods__[self.__name__](number_of_errors, number_of_values)

    def compute_differences_report (self):
        assert (self.file1 != None)
        assert (self.file2 != None)

        except Exception as e:
            self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
            return False, file_comparison.report_generator.generate_report_1_file (self.file1, self.file2, self.__name__, self.score, self.differences_report)
