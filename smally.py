#!/usr/bin/env python3
import sys
import os
import subprocess


def shcmd(cmd, shell=False):
    """execute a cmd without shell,
    return returncode, stdout, stderr"""
    proc = subprocess.run(cmd if shell else cmd.split(),
                          shell=shell,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def is_progressive(pathname):
    """check if pathname is progressive jpg format"""
    cmd = 'file %s | grep progressive' % pathname
    code, _, _ = shcmd(cmd, shell=True)
    if code == 0:
        return True
    return False


def jpegtran(pathname):
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        # baseline
        file_1 = wd + '/'+ basename + '.smally.jpg.baseline'
        cmd_1 = 'jpegtran -copy none -optimize -outfile %s %s'\
                                                        % (file_1, pathname)
        shcmd(cmd_1)
        # progressive
        file_2 = wd + '/' + basename + 'smally.jpg.progressive'
        cmd_2 = 'jpegtran -copy none -progressive -optimize -outfile %s %s'\
                                                        % (file_2, pathname)
        shcmd(cmd_2)
        # get jpg type
        progressive = is_progressive(pathname)
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
        _, mtime, _ = shcmd('stat -c "%y" ' + pathname)
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
            shcmd('touch -m -d "'+mtime.decode()+'" '+pathname)
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


def optipng(pathname):
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        out_file = wd + '/' + basename + '.smally.png'
        cmd = 'optipng -fix -%s %s -out %s'%('-o7 -zm1-9',pathname,out_file)
        shcmd(cmd)
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
            _, mtime, _ = shcmd('stat -c "%y" ' + pathname)
            os.remove(pathname)
            os.rename(out_file, pathname)
            shcmd('touch -m -d "'+mtime.decode()+'" '+pathname)
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


def gifsicle(pathname):
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(os.path.abspath(pathname))
        out_file = wd + '/' + basename + '.smally.gif'
        cmd = 'gifsicle -O3 --colors 256 %s -o %s'%(pathname, out_file)
        shcmd(cmd)
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
            _, mtime, _ = shcmd('stat -c "%y" ' + pathname)
            os.remove(pathname)
            os.rename(out_file, pathname)
            shcmd('touch -m -d "'+mtime.decode()+'" '+pathname)
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


# python3 smally.py --jpegtran|--optipng <filename>
if __name__ == '__main__':
    if sys.argv[1] == '--jpegtran':
        jpegtran(sys.argv[2])
    elif sys.argv[1] == '--optipng':
        optipng(sys.argv[2])
    elif sys.argv[1] == '--gifsicle':
        gifsicle(sys.argv[2])
    elif sys.argv[1] == '-V':
        print('smally V0.50 by xinlin-z (https://github.com/xinlin-z/smally)')
    else:
        print('Command line error.')

