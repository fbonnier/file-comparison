import os
import file_comparison.file_compare as fc
import file_comparison.nilsimsa as nl
import file_comparison.npz as npz
import file_comparison.neo as neo
import file_comparison.hamming as hm
import file_comparison.levenshtein as lv
import file_comparison.report_generator as report
import file_comparison.downloader as downloader
import profile
import argparse
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Computes file comparison using ')
    parser.add_argument('files', type=argparse.FileType('r'), metavar='files', nargs='+',
                        help='Files to compare')
    parser.add_argument('--hamming', dest='hamming', action='store_const',
                        const=hm.hamming_files,
                        help='Find the Hamming distance using bit comparison')
    parser.add_argument('--fuzzy', dest='fuzzy', action='store_const',
                        const=lv.levenshtein,
                        help='Find the Levenshtein distance using FuzzyWuzzy module')
    parser.add_argument('--nilsimsa', dest='nilsimsa', action='store_const',
                        const=nl.nilsimsa_files,
                        help='Find the Nilsimsa hash using nilsimsa module')
    parser.add_argument('--npz', dest='npz', action='store_const',
                        const=npz.npz_values,
                        help='Find the differences between two NPZ files')
    parser.add_argument('--neo', dest='neo', action='store_const',
                        const=neo.compare_neo_file,
                        help='Find the differences between two NEO files')
    parser.add_argument('--finfo', dest='finfo', action='store_const',
                        const=fc.hash_from_file_info,
                        help='Hash from file infos')
    parser.add_argument('--bijective', dest='bijective', action='store_const',
                        const=fc.find_bijective,
                        help='Hash from file infos')
    parser.add_argument('--profile', dest='profile', action='store_true',
                        help='Profiling the method')
    parser.add_argument('--buffersize', type=int, metavar='Buffer_Size', nargs=1, dest='buffersize', default=32,
                        help='Size of buffer used in bytes (default is 32 bytes)')
    parser.add_argument('--hex', type=int, metavar='Hexadigest_option', nargs=1, dest='hex', default=1,
                        help='Option to specify the files that contains hexadigest filenames.\n\
                        0: Both files contain plain urls and complete paths of result files\n\
                        1: First file contains urls that should be hashed to retreive corresponding filenames\n\
                        2: Both files contain urls/paths that should be hashed to retreive corresponding filenames')

    args = parser.parse_args()
    print (args)

    method = ""
    if args.hamming:
        method = "hamming"
    elif args.fuzzy:
        method = "fuzzy"
    elif args.nilsimsa:
        method = "nilsimsa"
    elif args.npz:
        method = "npz"
    elif args.neo:
        method = "neo"
    elif args.finfo:
        method = "finfo"

    # Build Adjacency Matrix from list of files
    # The matrix is compacted as a list of pairs
    adjacency_matrix = fc.find_bijective (args.files[0].name, args.files[1].name, args.hex[0])
    # print (adjacency_matrix)

    # Get adviced method
    advice_methods = fc.get_adviced_method (adjacency_matrix)

    

    # if advice_method != method:
    #     print ("Warning: Advice method and chosen are differents")
    #     print ("Advice method: " + advice_method)
    #     print ("Chosen method: " + method)
    #     print ("Warning: it is recommended to use adviced method. Chosen method is used in this run.")
    #     print ("\n")

    # print ("\nCOUPLES ::\n")
    # for tuple_left, tuple_right  in adjacency_matrix:
    #     print (tuple_left)
    #     print (tuple_right)
    #     print ("\n")

    final_report = []
    # Compare the files
    for icouple, imethod in zip(adjacency_matrix, advice_methods):
        # print(icouple, imethod)
        score, file_diff = report.compute_differences(icouple[0], icouple[1], imethod)
        final_report.append(report.generate_report_1_file (icouple[0], icouple[1], imethod, score, file_diff))


    # Generate Comparison Report
    # for ifile1, ifile2 in adjacency_matrix:
    #     final_report.append(report.generate_report_1_file (ifile1, ifile2, method, score, differences))

    print ("FINAL REPORT:")
    print (json.dumps(final_report, indent=4))

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
