# Method class
from file_comparison.file_compare import FileInfo

methods = ["npz", "neo", "byte"]

class Method:

    __name__ = ""
    file1 = ""
    file2 = ""
    score = 0.
    differences_report = []

    def __init__ (self, name, file_info_1, file_info_2):
        assert (name in methods)
        self.__name__ = name
        self.file1 = file_info_1
        self.file2 = file_info_2

    def compute_score (self):
        pass

    def compute_differences_report (self):
        assert (self.file1 != "")
        assert (self.file2 != "")
