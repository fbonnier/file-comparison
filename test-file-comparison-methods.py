import os

import file_compare as fc
import profile
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Computes file comparison using ')
    parser.add_argument('files', type=argparse.FileType('r'), metavar='files', nargs='+',
                        help='Files to compare')
    parser.add_argument('--hamming', dest='hamming', action='store_const',
                        const=fc.hamming_files,
                        help='Find the Hamming distance using bit comparison')
    parser.add_argument('--fuzzy', dest='fuzzy', action='store_const',
                        const=fc.fuzzy_files_light,
                        help='Find the Levenshtein distance using FuzzyWuzzy module')
    parser.add_argument('--nilsimsa', dest='nilsimsa', action='store_const',
                        const=fc.nilsimsa_files,
                        help='Find the Nilsimsa hash using nilsimsa module')
    parser.add_argument('--npz', dest='npz', action='store_const',
                        const=fc.npz_values,
                        help='Find the differences between two NPZ files')
    parser.add_argument('--finfo', dest='finfo', action='store_const',
                        const=fc.hash_from_file_info,
                        help='Hash from file infos')

    args = parser.parse_args()
    print (args)

    # Test Levenstein comparison
    # profile.run('print(fc.fuzzy_files_light ("./nest_400x400_pss_3_grid.npz", "./nest_400x400_pss_3_prod.npz")); print()')
    if args.hamming:
        profile.run('print(args.hamming(args.files[0].name, args.files[1].name)); print()')
    elif args.fuzzy:
        profile.run('print(args.fuzzy(args.files[0].name, args.files[1].name)); print()')
    elif args.nilsimsa:
        profile.run('print(args.nilsimsa(args.files[0].name, args.files[1].name)); print()')
    elif args.npz:
        profile.run('print(args.npz(args.files[0].name, args.files[1].name)); print()')
    elif args.finfo:
        profile.run('print(args.finfo(args.files[0].name, args.files[1].name)); print()')
