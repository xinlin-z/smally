#!/usr/bin/env python3 
import os
import sys
import argparse
import textwrap
from classes import sh, pShow, pSize, pJpegtran, NAME 


# contants
VER = '%s: compress JPGs losslessly in batch mode and more... V0.19 ' % NAME


def main():
    parser = argparse.ArgumentParser(
                formatter_class = argparse.RawDescriptionHelpFormatter,
                description = VER + textwrap.dedent('''
    
    Usage Examples:

    1), compress JPGs lossless in batch mode
        $ python3 smally.py -a /path1 /path2 --jpegtran --jpg
        -a option is mandatory and must have one absolute path at least.
        Only --jpg can be combined with --jpegtran.

    2), add interval time between each picture processed
        $ python3 smally.py -a /path1 --jpegtran --jpg -i 500
        Default interval time is zero.
        -i option is optional and in milliseconds unit.

    3), recursive action
        $ python3 smally.py -a /path1 --jpegtran --jpg -r
        -r option indicates the recursive action.
        Default behavior is not recursive, in line with other cmd tools.
    '''),
                epilog = 'welcome to my github & blog:\n'
                         'https://github.com/xinlin-z\n'
                         'https://www.maixj.net\n'
                         'https://www.pynote.net')
    
    parser.add_argument('-a', '--abspath', required=True, nargs='+', 
                    help='absolute path for the picture folder, support ~')
    parser.add_argument('-i', '--interval', type=int,
                        help='interval time in milliseconds')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='recursive into sub-folders')
    parser.add_argument('--jpg', action='store_true', 
                            help='for both .jpg and .jpeg suffix')
    parser.add_argument('--png', action='store_true')
    parser.add_argument('--gif', action='store_true')
    parser.add_argument('--webp', action='store_true')
    # group for action type
    actType = parser.add_mutually_exclusive_group(required=True)
    actType.add_argument('--show', action='store_true',
                        help='show pathname and size in KB')
    actType.add_argument('--size', action='store_true',
                        help='calculate total size')
    actType.add_argument('--jpegtran', action='store_true',
                help='lossless compress JPGs with jpegtran tool')
    # version info
    parser.add_argument('-V','--version',action='version',version=VER)
    args = parser.parse_args()  # ~ will be expanded
    # check path
    for path in args.abspath:
        if (not os.path.isabs(path) or
            not os.path.exists(path)):
            print('%s: All paths must be absolute and existed.' % NAME)
            sys.exit(1)
    # check picture type
    ptype = []
    if args.jpg: ptype.extend(['.jpg','.jpeg'])
    if args.png: ptype.append('.png')
    if args.gif: ptype.append('.gif')
    if args.webp: ptype.append('.webp')
    if ptype == []:
        print('%s: No picture type choosed.' % NAME)
        sys.exit(1)
    # interval
    interval = 0.0
    if args.interval != None:
        if args.interval >= 0: interval = args.interval/1000
        else: 
            print('%s: Interval time must be positive.' % NAME)
            sys.exit(1)
    # actions 
    if args.show: 
        if sh.which('identify') is False: sys.exit(1) 
        pShow(ptype, interval, args.recursive, args.abspath)
    if args.size:
        pSize(ptype, interval, args.recursive, args.abspath)
    if args.jpegtran:
        if ptype != ['.jpg','.jpeg']:
            print('%s: --jpegtran only support JPG.' % NAME)
            sys.exit(1)
        if sh.which('jpegtran') is False: sys.exit(1)
        if sh.which('identify') is False: sys.exit(1)
        pJpegtran(ptype, interval, args.recursive, args.abspath)


if __name__ == '__main__':
    main()


