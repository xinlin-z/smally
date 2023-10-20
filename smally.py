#!/usr/bin/env python3
"""
Compress JPEG, PNG and GIF losslessly by jpegtran, optipng and gifsicle.

Author:   xinlin-z
Github:   https://github.com/xinlin-z/smally
Blog:     https://cs.pynote.net
License:  MIT
"""
import sys
import os
import subprocess
import argparse
import multiprocessing as mp


def _cmd(cmd: str, shell: bool=False) -> tuple[int,bytes,bytes]:
    """ execute a command w/o shell,
        return returncode, stdout, stderr """
    proc = subprocess.run(cmd if shell else cmd.split(),
                          shell=shell,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def is_jpeg_progressive(pathname: str) -> bool:
    """ check if pathname is progressive jpg format """
    cmdstr = 'file %s | grep progressive' % pathname
    code, _, _ = _cmd(cmdstr, shell=True)
    return code == 0


def jpegtran(pathname: str) -> tuple[int,int]:
    """ use jpegtran to compress pathname,
        return tuple (saved, orginal_size). """
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        # baseline
        file_1 = wd + '/'+ basename + '.smally.jpg.baseline'
        cmd_1 = 'jpegtran -copy none -optimize -outfile %s %s'\
                                                        % (file_1, pathname)
        _cmd(cmd_1)
        # progressive
        file_2 = wd + '/' + basename + '.smally.jpg.progressive'
        cmd_2 = 'jpegtran -copy none -progressive -optimize -outfile %s %s'\
                                                        % (file_2, pathname)
        _cmd(cmd_2)
        # get jpg type
        progressive = is_jpeg_progressive(pathname)
        # choose the smallest one
        size = os.path.getsize(pathname)
        size_1 = os.path.getsize(file_1)
        size_2 = os.path.getsize(file_2)
        if size <= size_1 and size <= size_2:
            select_file = 0
            if size == size_2 and progressive is False:
                select_file = 2  # progressive is preferred
        else:
            if size_2 <= size_1: select_file = 2
            else: select_file = 1
        # get mtime
        _, mtime, _ = _cmd('stat -c "%y" ' + pathname)
        # rm & mv
        if select_file == 0:  # origin
            os.remove(file_1)
            os.remove(file_2)
            saved = 0
        elif select_file == 1:  # baseline
            os.remove(pathname)
            os.remove(file_2)
            os.rename(file_1, pathname)
            saved = size_1 - size
        else:  # select_file == 2:  # progressive
            os.remove(pathname)
            os.remove(file_1)
            os.rename(file_2, pathname)
            saved = size_2 - size
        # keep mtime
        if select_file != 0:
            _cmd('touch -m -d "'+mtime.decode()+'" '+pathname)
        return saved, size
    except BaseException:
        try:
            if os.path.exists(pathname):
                try: os.remove(file_1)
                except FileNotFoundError: pass
                try: os.remove(file_2)
                except FileNotFoundError: pass
            else:
                if (os.path.exists(file_1) and
                        os.path.exists(file_2)):
                    if os.path.getsize(file_1) >= os.path.getsize(file_2):
                        os.remove(file_1)
                        os.rename(file_2, pathname)
                    else:
                        os.remove(file_2)
                        os.rename(file_1, pathname)
                elif os.path.exists(file_2):
                    os.rename(file_2, pathname)
                else: os.rename(file_1, pathname)
        except UnboundLocalError:
            pass
        raise


def optipng(pathname: str) -> tuple[int,int]:
    """ use optipng to compress pathname,
        return tuple (saved, orginal_size). """
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        out_file = wd + '/' + basename + '.smally.png'
        cmds = 'optipng -fix -%s %s -out %s'%('-o7 -zm1-9',pathname,out_file)
        _cmd(cmds)
        size_1 = os.path.getsize(pathname)
        size_2 = os.path.getsize(out_file)
        if size_1 == size_2:
            os.remove(out_file)
            saved = 0
        else:
            saved = size_2 - size_1
            _, mtime, _ = _cmd('stat -c "%y" ' + pathname)
            os.remove(pathname)
            os.rename(out_file, pathname)
            _cmd('touch -m -d "'+mtime.decode()+'" '+pathname)
        return saved, size_1
    except BaseException:
        try:
            if os.path.exists(pathname):
                os.remove(out_file)
            elif os.path.exists(out_file):
                os.rename(out_file, pathname)
        except FileNotFoundError:
            pass
        raise


def gifsicle(pathname: str) -> tuple[int,int]:
    """ use gifsicle to compress pathname,
        return tuple (saved, orginal_size). """
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        out_file = wd + '/' + basename + '.smally.gif'
        cmdstr = 'gifsicle -O3 --colors 256 %s -o %s' % (pathname, out_file)
        _cmd(cmdstr)
        size_1 = os.path.getsize(pathname)
        size_2 = os.path.getsize(out_file)
        if size_1 <= size_2:
            os.remove(out_file)
            saved = 0
        else:
            saved = size_2 - size_1
            _, mtime, _ = _cmd('stat -c "%y" ' + pathname)
            os.remove(pathname)
            os.rename(out_file, pathname)
            _cmd('touch -m -d "'+mtime.decode()+'" '+pathname)
        return saved, size_1
    except BaseException:
        try:
            if os.path.exists(pathname):
                os.remove(out_file)
            elif os.path.exists(out_file):
                os.rename(out_file, pathname)
        except FileNotFoundError:
            pass
        raise


def _show(ftype: str, pathname: str, saved: tuple[int,int]) -> None:
    if saved[0] == 0:
        logstr = '--'
    else:
        logstr = str(saved[0]) +' '+ str(round(saved[0]/saved[1]*100,2)) + '%'
    progressive = '' if ftype!='j' else \
                    ('[b]','[p]')[is_jpeg_progressive(pathname)]
    print(' '.join((pathname, logstr, progressive)))


def _find_xargs(pnum: int, ftype: str='') -> None:
    pnum = max(1, pnum)
    print('# parallel process number: ', pnum)
    cmdstr = 'find %s -type f -print0 | '\
             'xargs -P%d -I! -0 python %s %s !' \
             % (args.pathname, pnum, sys.argv[0], ftype)
    proc = subprocess.Popen(cmdstr, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    for line in iter(proc.stdout.readline, b''):
        print(line.decode(), end='')


_VER = 'smally V0.53 by xinlin-z \
        (https://github.com/xinlin-z/smally)'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=_VER)
    ftype = parser.add_mutually_exclusive_group()
    ftype.add_argument('-j', '--jpegtran', action='store_true',
                       help='use jpegtran to compress jpeg file')
    ftype.add_argument('-p', '--optipng', action='store_true',
                       help='use optipng to compress png file')
    ftype.add_argument('-g', '--gifsicle', action='store_true',
                       help='use gifsicle to compress gif file')
    parser.add_argument('pathname', help='specify the pathname')
    parser.add_argument('-P', type=int, default=mp.cpu_count(),
                        help='process number, default is by cpu_count')
    args = parser.parse_args()

    # get pathname type
    cmdstr = "file %s | awk '{print $2}'" % args.pathname
    rcode, stdout, stderr = _cmd(cmdstr, shell=True)
    if rcode != 0:
        # pathname might contains unusual chars, here is test
        print('# error occure while processing %s' % args.pathname)
        print(stderr.decode(), end='')
        sys.exit(rcode)
    pathname_type = stdout.decode().strip()
    if pathname_type not in ('JPEG','PNG','GIF','directory'):
        sys.exit(1)

    # if type specified
    if args.jpegtran or args.optipng or args.gifsicle:
        if args.jpegtran and pathname_type=='JPEG':
            _show('j', args.pathname, jpegtran(args.pathname))
        elif args.optipng and pathname_type=='PNG':
            _show('p', args.pathname, optipng(args.pathname))
        elif args.gifsicle and pathname_type=='GIF':
            _show('g', args.pathname, gifsicle(args.pathname))
        elif pathname_type == 'directory':
            file_type = '-j' if args.jpegtran else \
                        '-p' if args.optipng else '-g'
            _find_xargs(args.P, file_type)
        else:
            sys.exit(1)
        sys.exit(0)

    # no type specified
    if pathname_type == 'JPEG':
        _show('j', args.pathname, jpegtran(args.pathname))
    elif pathname_type == 'PNG':
        _show('p', args.pathname, optipng(args.pathname))
    elif pathname_type == 'GIF':
        _show('g', args.pathname, gifsicle(args.pathname))
    elif pathname_type == 'directory':
        _find_xargs(args.P)
    sys.exit(0)

