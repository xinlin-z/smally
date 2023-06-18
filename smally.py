#!/usr/bin/env python3
"""
Compress jpeg, png and gif losslessly by jpegtran, optipng and gifsicle.

Author:   xinlin-z
Github:   https://github.com/xinlin-z/smally
Blog:     https://cs.pynote.net
License:  MIT
"""
import sys
import os
import subprocess
import argparse


def cmd(cmd: str, shell: bool=False) -> tuple[int,bytes,bytes]:
    """execute a cmd w/o shell,
    return returncode, stdout, stderr"""
    proc = subprocess.run(cmd if shell else cmd.split(),
                          shell=shell,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def is_jpeg_progressive(pathname: str) -> bool:
    """check if pathname is progressive jpg format"""
    cmdstr = 'file %s | grep progressive' % pathname
    code, _, _ = cmd(cmdstr, shell=True)
    return True if code==0 else False


def jpegtran(pathname: str) -> None:
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        # baseline
        file_1 = wd + '/'+ basename + '.smally.jpg.baseline'
        cmd_1 = 'jpegtran -copy none -optimize -outfile %s %s'\
                                                        % (file_1, pathname)
        cmd(cmd_1)
        # progressive
        file_2 = wd + '/' + basename + 'smally.jpg.progressive'
        cmd_2 = 'jpegtran -copy none -progressive -optimize -outfile %s %s'\
                                                        % (file_2, pathname)
        cmd(cmd_2)
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
        _, mtime, _ = cmd('stat -c "%y" ' + pathname)
        # rm & mv
        _log = pathname + ' '
        if select_file == 0:  # origin
            os.remove(file_1)
            os.remove(file_2)
            if progressive is True:
                _log += '-- [p]'
            else:
                _log += '-- [b]'
        elif select_file == 1:  # baseline
            os.remove(pathname)
            os.remove(file_2)
            os.rename(file_1, pathname)
            saved = size - size_1
            _log += '-' + str(saved) \
                        + ' -' + str(round(saved/size*100,2)) + '%' \
                        + ' [b]'
        else:  # select_file == 2:  # progressive
            os.remove(pathname)
            os.remove(file_1)
            os.rename(file_2, pathname)
            saved = size - size_2
            _log += '-' + str(saved) \
                        + ' -' + str(round(saved/size*100,2)) +'%' \
                        + ' [p]'
        # keep mtime
        if select_file != 0:
            cmd('touch -m -d "'+mtime.decode()+'" '+pathname)
        # log and count
        print(_log)
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


def optipng(pathname: str) -> None:
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        out_file = wd + '/' + basename + '.smally.png'
        cmdstr = 'optipng -fix -%s %s -out %s'%('-o7 -zm1-9',pathname,out_file)
        cmd(cmdstr)
        _log = pathname + ' '
        size_1 = os.path.getsize(pathname)
        size_2 = os.path.getsize(out_file)
        if size_1 == size_2:
            _log += '--'
            os.remove(out_file)
        else:
            saved = size_1 - size_2
            sym = '-' if saved > 0 else '+'
            fixed = '' if saved > 0 else 'fixed'
            _log += sym + str(abs(saved)) \
                        + ' ' + sym \
                        + str(round(abs(saved)/size_1*100,2)) \
                        + '%' + fixed
            _, mtime, _ = cmd('stat -c "%y" ' + pathname)
            os.remove(pathname)
            os.rename(out_file, pathname)
            cmd('touch -m -d "'+mtime.decode()+'" '+pathname)
        print(_log)
    except BaseException:
        try:
            if os.path.exists(pathname):
                os.remove(out_file)
            elif os.path.exists(out_file):
                os.rename(out_file, pathname)
        except FileNotFoundError:
            pass
        raise


def gifsicle(pathname: str) -> None:
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        out_file = wd + '/' + basename + '.smally.gif'
        cmdstr = 'gifsicle -O3 --colors 256 %s -o %s'%(pathname, out_file)
        cmd(cmdstr)
        _log = pathname + ' '
        size_1 = os.path.getsize(pathname)
        size_2 = os.path.getsize(out_file)
        if size_1 <= size_2:
            _log += '--'
            os.remove(out_file)
        else:
            saved = size_1 - size_2
            sym = '-' if saved > 0 else '+'
            _log += sym + str(abs(saved)) \
                        + ' ' + sym \
                        + str(round(abs(saved)/size_1*100,2))\
                        + '%'
            _, mtime, _ = cmd('stat -c "%y" ' + pathname)
            os.remove(pathname)
            os.rename(out_file, pathname)
            cmd('touch -m -d "'+mtime.decode()+'" '+pathname)
        print(_log)
    except BaseException:
        try:
            if os.path.exists(pathname):
                os.remove(out_file)
            elif os.path.exists(out_file):
                os.rename(out_file, pathname)
        except FileNotFoundError:
            pass
        raise


def _show(file_type: str,
          pathname: str,
          saved: tuple[int,float]) -> None:
    _log =(pathname
           + ' '
           + '--' if saved[0]==0 else str(saved[0])+' '+str(round(saved[1],2))
           + ' '
           + '' if file_type!='j' else
                        '[p]' if is_jpeg_progressive(pathname) else '[b]')
    print(_log)


_VER = 'smally V0.52 by xinlin-z (https://github.com/xinlin-z/smally)'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=_VER)
    file_type = parser.add_mutually_exclusive_group(required=True)
    file_type.add_argument('-j', '--jpegtran', action='store_true',
                           help='use jpegtran to compress jpeg file')
    file_type.add_argument('-p', '--optipng', action='store_true',
                           help='use optipng to compress png file')
    file_type.add_argument('-g', '--gifsicle', action='store_true',
                           help='use gifsicle to compress gif file')
    parser.add_argument('pathname', help='specify the pathname')
    args = parser.parse_args()

    if args.jpegtran:
        jpegtran(args.pathname)
    elif args.optipng:
        optipng(args.pathname)
    elif args.gifsicle:
        gifsicle(args.pathname)

