#!/usr/bin/env python3 
import os
import sys
import argparse
from classes import sh, pShow, pSize, pJpegtran, NAME 


# contants
VER = '%s: compress JPGs losslessly in batch mode and more... V0.18 '\
            'by www.pynote.net' % NAME


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--abspath', required=True, 
                        help='absolute path for the picture folder')
    parser.add_argument('-i', '--interval', type=int,
                        help='interval time in milliseconds')
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
    if (not os.path.isabs(args.abspath) or
        not os.path.exists(args.abspath)):
        print('%s: path must be absolute and existed, support ~' % NAME)
        sys.exit(1)
    # check picture type
    ptype = []
    if args.jpg: ptype.extend(['.jpg','.jpeg'])
    if args.png: ptype.append('.png')
    if args.gif: ptype.append('.gif')
    if args.webp: ptype.append('.webp')
    if ptype == []:
        print('%s: no picture type choosed' % NAME)
        sys.exit(1)
    # interval
    interval = 0.0
    if args.interval != None:
        if args.interval >= 0: interval = args.interval/1000
        else: 
            print('%s: interval time must be positive' % NAME)
            sys.exit(1)
    # actions 
    if args.show: 
        if sh.which('identify') is False: sys.exit(1) 
        pShow(ptype, interval, (args.abspath,))
    if args.size:
        pSize(ptype, interval, (args.abspath,))
    if args.jpegtran:
        if ptype != ['.jpg','.jpeg']:
            print('%s: --jpegtran only support JPG' % NAME)
            sys.exit(1)
        if sh.which('jpegtran') is False: sys.exit(1)
        if sh.which('identify') is False: sys.exit(1)
        pJpegtran(ptype, interval, (args.abspath,))


if __name__ == '__main__':
    main()


