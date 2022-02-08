import os
import file_comparison.file_compare as fc
import file_comparison.nilsimsa as nl
import file_comparison.npz as npz
import file_comparison.neo as neo
import file_comparison.hamming as hm
import file_comparison.levenshtein as lv
import file_comparison.downloader as downloader
import profile
import argparse

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

    if args.bijective:
        args.bijective(args.files[0].name, args.files[1].name, args.hex[0])

    if args.profile:
        if args.hamming:
            profile.run('args.hamming(args.files[0].name, args.files[1].name, args.buffersize)')
        elif args.fuzzy:
            profile.run('args.fuzzy(args.files[0].name, args.files[1].name, args.buffersize)')
        elif args.nilsimsa:
            profile.run('args.nilsimsa(args.files[0].name, args.files[1].name, args.buffersize)')
        elif args.npz:
            profile.run('args.npz(args.files[0].name, args.files[1].name')
        elif args.neo:
            profile.run('args.neo(args.files[0].name, args.files[1].name')
        elif args.finfo:
            profile.run('args.finfo(args.files[0].name, args.files[1].name)')
    else:
        if args.hamming:
            args.hamming(args.files[0].name, args.files[1].name, args.buffersize)
        elif args.fuzzy:
            args.fuzzy(args.files[0].name, args.files[1].name, args.buffersize)
        elif args.nilsimsa:
            args.nilsimsa(args.files[0].name, args.files[1].name, args.buffersize)
        elif args.npz:
            args.npz(args.files[0].name, args.files[1].name)
        elif args.neo:
            args.neo(args.files[0].name, args.files[1].name)
        elif args.finfo:
            args.finfo(args.files[0].name, args.files[1].name)
