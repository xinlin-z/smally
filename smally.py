import os
import sys
import logging
import argparse
import textwrap
from classes import sh, pShow, pSize, pJpegtran, pOptipng, NAME


log = logging.getLogger()  # get root logger
logging.basicConfig(stream=sys.stdout,
                    format="%(message)s", level=logging.INFO)


# contants
VER = '%s: compress JPG & PNG losslessly in batch mode and more... V0.23'\
      % NAME


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=VER + textwrap.dedent('''

    Usage Examples:

    1), compress JPG losslessly with jpegtran in batch mode
        $ python3 smally.py -p path1 path2 --jpegtran --jpg
        -p option is mandatory and must have one path argument at least.
        Only --jpg can be combined with --jpegtran.

    2), add interval time between each picture processed
        $ python3 smally.py -p path1 --jpegtran --jpg -i 500
        Default interval time is zero.
        -i option is optional and in milliseconds unit.

    3), recurse into sub-folders
        $ python3 smally.py -p path1 --jpegtran --jpg -r
        -r option indicates the recursive action.
        Default behavior is not recursive, in line with other cmd tools.

    4), keep mtime unchanged
        $ python3 smally.py -p path1 --jpegtran --jpg -k
        -k option indicates the mtime would not be changed while the
        compressing process. By default, new compressed file will get a new
        mtime stamp.

    5), set time window to skip old file in your routine
        $ python3 smally.py -p path1 --jpegtran --jpg -t 86400
        -t 86400 means the time window is 1 day. If the distance between
        file mtime and NOW is within this specific time window, action will
        be applied to this file, otherwise it will be skipped.
        To keep mtime of compressed file unchanged, you need -k option.
        -t is optional, time window is infinite if not configured.

    6), calculate size
        $ python3 smally.py -p path --size --jpg
        Calculate the total JPGs size in /path. You can combine --size with
        -r, -i, -t option. -k option is useless with --size.
        $ python3 smally.py -p path --size --jpg --png --gif --webp
        Calculate the total size of all 4 types of pictures.

    7), show info of picture file
        $ python3 smally.py -p path --show --jpg --png
        Show all JPGs and PNGs in path. You can combine --show with
        -r, -t option. -k option is useless with --show.

    8), show other files
        $ python3 smally.py -p path --show -r
        Show other files in path, more info in README.md.

    9), compress PNG losslessly with optipng in batch mode
        $ python3 smally.py -p path1 path2 --optipng o2 --png

    10), file mode
        $ python3 smally.py -f file1 file2 --show --jpg --png
        $ python3 smally.py -f file1 file2 --size --jpg --png
        $ python3 smally.py -f file1 file2 --jpegtran --jpg
        $ python3 smally.py -f file1 file2 --optipng o2 --png
        -f: file mode
    '''),
        epilog='smally project page: '
               'https://github.com/xinlin-z/smally\n'
               'author\'s python note blog: '
               'https://www.pynote.net'
    )
    # group for path or file
    pfType = parser.add_mutually_exclusive_group(required=True)
    pfType.add_argument('-p', '--paths', nargs='+',
                        help='paths for the picture folder')
    pfType.add_argument('-f', '--files', nargs='+',
                        help='picture files')
    #
    parser.add_argument('-i', type=int, metavar='INTERVAL', dest='interval',
                        help='interval time in milliseconds')
    parser.add_argument('-r', action='store_true', dest='recursive',
                        help='recursive into sub-folders')
    parser.add_argument('-k', action='store_true', dest='keepmtime',
                        help='keep the mtime untouched after compressing')
    parser.add_argument('-t', type=float,
                        metavar='TIMEWINDOW', dest='timewindow',
                        help='apply action to files those Now - mtime is '
                             'in time window (seconds, float and positive)')
    # picture types
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
                         help='lossless compress JPGs with jpegtran')
    actType.add_argument(
        '--optipng',
        choices=['o0','o1','o2','o3','o4','o5','o6','o7','o7 -zm1-9'],
        help='lossless compress PNGs with optipng')
    # version
    parser.add_argument('-V','--version',action='version',version=VER)
    args = parser.parse_args()  # ~ will be expanded
    # check paths or files
    if args.paths is not None:
        for path in args.paths:
            if not os.path.exists(path):
                log.info('%s: path %s is not existed.' % (NAME,path))
                sys.exit(1)
    else:
        file_exts = set()
        for sfile in args.files:
            _, ext = os.path.splitext(sfile)
            file_exts.add(ext.lower())
            if not os.path.exists(sfile):
                log.info('%s: file %s is not existed.' % (NAME,sfile))
                sys.exit(1)
    # check picture type
    ptype = []
    if args.jpg: ptype.extend(['.jpg','.jpeg'])
    if args.png: ptype.append('.png')
    if args.gif: ptype.append('.gif')
    if args.webp: ptype.append('.webp')
    if ptype == [] and not args.show:
        log.info('%s: No picture type choosed.' % NAME)
        sys.exit(1)
    if ptype == [] and args.show and args.files:
        log.info('%s: No picture type choosed.' % NAME)
        sys.exit(1)
    if args.files:
        if not file_exts <= set(ptype):
            log.info('%s: input files are not in picture type choosed.'%NAME)
            sys.exit(1)
    # interval
    interval = 0.0
    if args.interval is not None:
        if args.interval >= 0: interval = args.interval/1000
        else:
            log.info('%s: Interval time must be positive.' % NAME)
            sys.exit(1)
    # time window
    if args.timewindow is not None:
        if args.timewindow <= 0:
            log.info('%s: Time window must be positive.' % NAME)
            sys.exit(1)
        if args.files:
            log.info('%s: Time window will be ignored when -f.' % NAME)
    # actions
    if sh.which('identify') is False: sys.exit(1)
    if args.show:
        pShow(ptype, interval, args.recursive, args.timewindow,
              args.paths, args.files)
    if args.size:
        pSize(ptype, interval, args.recursive, args.timewindow,
              args.paths, args.files)
    if args.jpegtran:
        if ptype != ['.jpg','.jpeg']:
            log.info('%s: --jpegtran only support JPG.' % NAME)
            sys.exit(1)
        if sh.which('jpegtran') is False: sys.exit(1)
        pJpegtran(ptype, interval, args.recursive, args.timewindow,
                  args.paths, args.files, args.keepmtime)
    if args.optipng:
        if ptype != ['.png']:
            log.info('%s: --optipng only support PNG.' % NAME)
            sys.exit(1)
        if sh.which('optipng') is False: sys.exit(1)
        pOptipng(ptype, interval, args.recursive, args.timewindow,
                 args.paths, args.files, args.keepmtime, args.optipng)


if __name__ == '__main__':
    main()


