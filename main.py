import os
import file_comparison.file_compare as fc
import file_comparison.nilsimsa as nl
import file_comparison.npz as npz
import file_comparison.neo as neo
import file_comparison.hamming as hm
import file_comparison.levenshtein as lv
import file_comparison.report_generator as report
import file_comparison.downloader as downloader
import file_comparison.bijective as bijective
import file_comparison.method as method
import profile
import argparse
import json
import sys


def run_file_comparison_json (jsonfile):
    error_glob = None
    json_data = None
    pairs = None
    with open(jsonfile, "r") as f:
        json_data = json.load (f)
        try:
            method = ""

            # Build Adjacency Matrix from list of files
            # The matrix is compacted as a list of pairs
            pairs = bijective.find_bijective (json_data["Metadata"]["run"]["outputs"], json_data["Outputs"])

            # Get adviced method
            for ipair in pairs:
                ipair = method.get_adviced_method (ipair)

            # Final report to include to JSON file
            report_block = []

            # Compare the files
            for ipair in pairs:
                imethod = method.Method (ipair)
                
                # Check files format
                check, error = imethod.check_file_formats ()
                if not check:
                    # if the files are not the same format: Error
                    ipair["error"].append (error)
                    continue

                # Compute differences between data
                # error = imethod.compute_differences ()

                # Compute different scores and stats
                # imethod.compute_score ()

                # imethod.
                # ipair = imethod.topair(ipair)

            # for icouple, imethod in zip(adjacency_matrix, advice_methods):
            #     # print(icouple, imethod)
            #     # score, file_diff = report.compute_differences(icouple[0], icouple[1], imethod)
            #     # final_report.append(report.generate_report_1_file (icouple[0], icouple[1], imethod, score, file_diff))
            #     method = Method (imethod, icouple[0], icouple[1])
            #     is_checked, check_error = method.check_file_formats()

            #     # print (is_checked)
            #     if (is_checked):
            #         method.compute_differences_report()
            #         method.compute_score()
            #         report_block.append ({"f1": icouple[0].finfo_to_dict(), "f2": icouple[1], "Method": str(method.__name__), "score": "method.differences_report", "rmse": None, "mape": None, "mse": None, "report": None, "nerrors": 0, "ndiff": 0, "nvalues": 0})

        except Exception as e:
            error_glob = str(e)

    # Write data in JSON file
    with open(jsonfile, "w") as f:
        if json_data:
            json_data["Reusability Verification"] = {}
            json_data["Reusability Verification"]["error"] = error_glob
        
            json_data["Reusability Verification"]["files"] = pairs
    
            # Methods report
            json.dump(json_data, f, indent=4)
        
    # Exit Done ?
    sys.exit()
    # print (json.dumps(final_report, indent=4))





def run_file_comparison_files(file1, file2):


    method = ""

    # Build Adjacency Matrix from list of files
    # The matrix is compacted as a list of pairs
    adjacency_matrix = fc.find_bijective (args.files[0].name, args.files[1].name)

    # Get adviced method
    advice_methods = fc.get_adviced_method (adjacency_matrix)

    # Final report to include to JSON file
    final_report = []

    # Compare the files
    for icouple, imethod in zip(adjacency_matrix, advice_methods):
        # print(icouple, imethod)
        # score, file_diff = report.compute_differences(icouple[0], icouple[1], imethod)
        # final_report.append(report.generate_report_1_file (icouple[0], icouple[1], imethod, score, file_diff))
        method = Method (imethod, icouple[0], icouple[1])
        is_checked, check_error = method.check_file_formats()

        print (is_checked)
        if (is_checked):
            method.compute_differences_report()
            method.compute_score()
            final_report.append (method.differences_report)

    
    # print ("FINAL REPORT:")
    # print (json.dumps(final_report, indent=4))




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Computes file comparison using ')
    parser.add_argument('--files', type=argparse.FileType('r'), metavar='files', nargs=2,
                        help='Files to compare')
    parser.add_argument('--json', type=argparse.FileType('r'), metavar='json', nargs=1,
                        help='JSON File containing metadata of files to compare')
    # parser.add_argument('--watchdog', type=argparse.FileType('r'), metavar='watchdog', nargs='1',
    #                     help='Watchdog File containing files to compare with JSON report')
    # parser.add_argument('--hamming', dest='hamming', action='store_const',
    #                     const=hm.hamming_files,
    #                     help='Find the Hamming distance using bit comparison')
    # parser.add_argument('--fuzzy', dest='fuzzy', action='store_const',
    #                     const=lv.levenshtein,
                        # help='Find the Levenshtein distance using FuzzyWuzzy module')
    # parser.add_argument('--nilsimsa', dest='nilsimsa', action='store_const',
    #                     const=nl.nilsimsa_files,
    #                     help='Find the Nilsimsa hash using nilsimsa module')
    # parser.add_argument('--npz', dest='npz', action='store_const',
    #                     const=npz.npz_values,
    #                     help='Find the differences between two NPZ files')
    # parser.add_argument('--neo', dest='neo', action='store_const',
    #                     const=neo.compare_neo_file,
    #                     help='Find the differences between two NEO files')
    # parser.add_argument('--finfo', dest='finfo', action='store_const',
    #                     const=fc.hash_from_file_info,
    #                     help='Hash from file infos')
    # parser.add_argument('--bijective', dest='bijective', action='store_const',
    #                     const=fc.find_bijective,
    #                     help='Hash from file infos')
    parser.add_argument('--profile', dest='profile', action='store_true',
                        help='Profiling the method')
    # parser.add_argument('--buffersize', type=int, metavar='Buffer_Size', nargs=1, dest='buffersize', default=32,
    #                     help='Size of buffer used in bytes (default is 32 bytes)')
    # parser.add_argument('--hex', type=int, metavar='Hexadigest_option', nargs=1, dest='hex', default=1,
    #                     help='Option to specify the files that contains hexadigest filenames.\n\
    #                     0: Both files contain plain urls and complete paths of result files\n\
    #                     1: First file contains urls that should be hashed to retreive corresponding filenames\n\
    #                     2: Both files contain urls/paths that should be hashed to retreive corresponding filenames')

    args = parser.parse_args()
    jsonfile = args.json[0] if args.json else None

    file1 = args.files[0] if args.files else None
    file2 = args.files[1] if args.files else None
    
    if args.profile:
        if jsonfile:
            try:
                profile.run('run_file_comparison_json(jsonfile.name)')
            except Exception as e1:
                print (e1)
        elif file1 and file2:
            try:
                profile.run('run_file_comparison_files(file1.name, file2.name)')
            except Exception as e2:
                print (e2)

    else:
        if jsonfile:
            try:
                run_file_comparison_json(jsonfile.name)
            except Exception as e1:
                print (e1)
        elif file1 and file2:
            try:
                run_file_comparison_files(file1.name, file2.name)
            except Exception as e2:
                print (e2)
                

    # method = ""
    # if args.hamming:
    #     method = "hamming"
    # elif args.fuzzy:
    #     method = "fuzzy"
    # elif args.nilsimsa:
    #     method = "nilsimsa"
    # elif args.npz:
    #     method = "npz"
    # elif args.neo:
    #     method = "neo"
    # elif args.finfo:
    #     method = "finfo"

    # # Build Adjacency Matrix from list of files
    # # The matrix is compacted as a list of pairs
    # adjacency_matrix = fc.find_bijective (args.files[0].name, args.files[1].name, args.hex[0])
    # # print (adjacency_matrix)

    # # Get adviced method
    # advice_methods = fc.get_adviced_method (adjacency_matrix)

    # final_report = []
    # # Compare the files
    # for icouple, imethod in zip(adjacency_matrix, advice_methods):
    #     # print(icouple, imethod)
    #     # score, file_diff = report.compute_differences(icouple[0], icouple[1], imethod)
    #     # final_report.append(report.generate_report_1_file (icouple[0], icouple[1], imethod, score, file_diff))
    #     method = Method (imethod, icouple[0], icouple[1])
    #     is_checked, check_error = method.check_file_formats()

    #     print (is_checked)
    #     if (is_checked):
    #         method.compute_differences_report()
    #         method.compute_score()
    #         final_report.append (method.differences_report)


    # # Generate Comparison Report
    # # for ifile1, ifile2 in adjacency_matrix:
    # #     final_report.append(report.generate_report_1_file (ifile1, ifile2, method, score, differences))

    # print ("FINAL REPORT:")
    # print (json.dumps(final_report, indent=4))

    # if args.bijective:
    #     args.bijective(args.files[0].name, args.files[1].name, args.hex[0])
    #
    # if args.profile:
    #     if args.hamming:
    #         profile.run('args.hamming(args.files[0].name, args.files[1].name, args.buffersize)')
    #     elif args.fuzzy:
    #         profile.run('args.fuzzy(args.files[0].name, args.files[1].name, args.buffersize)')
    #     elif args.nilsimsa:
    #         profile.run('args.nilsimsa(args.files[0].name, args.files[1].name, args.buffersize)')
    #     elif args.npz:
    #         profile.run('args.npz(args.files[0].name, args.files[1].name')
    #     elif args.neo:
    #         profile.run('args.neo(args.files[0].name, args.files[1].name')
    #     elif args.finfo:
    #         profile.run('args.finfo(args.files[0].name, args.files[1].name)')
    # else:
    #     if args.hamming:
    #         args.hamming(args.files[0].name, args.files[1].name, args.buffersize)
    #     elif args.fuzzy:
    #         args.fuzzy(args.files[0].name, args.files[1].name, args.buffersize)
    #     elif args.nilsimsa:
    #         args.nilsimsa(args.files[0].name, args.files[1].name, args.buffersize)
    #     elif args.npz:
    #         args.npz(args.files[0].name, args.files[1].name)
    #     elif args.neo:
    #         args.neo(args.files[0].name, args.files[1].name)
    #     elif args.finfo:
    #         args.finfo(args.files[0].name, args.files[1].name)
