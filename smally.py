#!/usr/bin/env python3 
import os 
import sys
import argparse
from stat import *
import subprocess


def walktree(top, call):
    """walk file tree from position top, 
    for each file, callback is called.
    https://www.pynote.net/archives/294"""
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        try: 
            mode = os.stat(pathname, follow_symlinks=False).st_mode
        except:
            continue
        if S_ISDIR(mode):
            # directory, recurse into it
            walktree(pathname, call)
        else: 
            # skip all other file type but regular file
            if S_ISREG(os.stat(pathname).st_mode) is False: 
                return
            # get file extension
            _, file_ext = os.path.splitext(pathname)
            # call
            if (file_ext == '.jpg' or file_ext == '.jpeg') and JPG == True:
                call(pathname)
            if file_ext == '.png' and PNG == True:
                call(pathname)
            if file_ext == '.gif' and GIF == True:
                call(pathname)
            if file_ext == '.webp' and WEBP == True:
                call(pathname)
    return
    

def show_file(pathname):
    """show pathname accordingly"""
    size = os.path.getsize(pathname)
    if size <= 1024: print(pathname, size)
    else: print(pathname, str(round(size/1024,2))+'K') 
    return


def size_file(pathname):
    """calculate total size of picture choosed"""
    global SIZE
    SIZE += os.path.getsize(pathname)
    return


def isProgressive(pathname):
    """check if pathname is progressive jpg format"""
    cmd = 'identify -verbose %s | grep Interlace' % pathname
    proc = subprocess.run(cmd, shell=True,  
            stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    if proc.returncode != 0:
        print('%s: error while identify jpg format' % NAME)
        print(proc.stderr.decode())
        sys.exit(1)
    if proc.stdout.decode().find('None') == -1:  # progressive found
        return True
    return False


def jpegtran_jpg(pathname):
    """use jpegtran compress jpg losslessly"""
    print(pathname, end=' ')
    basename = os.path.basename(pathname)
    if basename[0] == '-':
        print('skip due to file name')
        return
    wd = os.path.dirname(pathname)
    # baseline 
    file_1 = '_1_' + basename
    cmd_1 = 'jpegtran -copy none -optimize %s > %s' % (basename,file_1)
    proc = subprocess.run(cmd_1, shell=True, cwd=wd, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    if proc.returncode != 0:
        print('%s: error while jpegtran baseline compression' % NAME)
        print(proc.stderr.decode())
        os.remove(wd+'/'+file_1)
        sys.exit(1)
    # progressive
    file_2 = '_2_' + basename
    cmd_2 = 'jpegtran -copy none -progressive %s > %s' % (basename,file_2)
    proc = subprocess.run(cmd_2, shell=True, cwd=wd, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    if proc.returncode != 0:
        print('%s: error while jpegtran progressive compression' % NAME)
        print(proc.stderr.decode())
        os.remove(wd+'/'+file_2)
        sys.exit(1)
    # choose the smallest one
    size = os.path.getsize(pathname)
    size_1 = os.path.getsize(wd+'/'+file_1)
    size_2 = os.path.getsize(wd+'/'+file_2)
    if size <= size_1 and size <= size_2: 
        select_file = 0
        if size == size_2 and isProgressive(pathname) is False: 
            select_file = 2  # progressive is preferred
    else:
        if size_2 <= size_1: select_file = 2  
        else: select_file = 1
    # rm & mv
    global SAVED
    try:
        if select_file == 0:  # origin
            os.remove(wd+'/'+file_1)
            os.remove(wd+'/'+file_2)
            if isProgressive(pathname) is True:
                print('-- [p]')
            else: print('-- [b]')
        if select_file == 1:  # baseline
            os.remove(pathname)
            os.remove(wd+'/'+file_2)
            os.rename(wd+'/'+file_1, pathname)
            print('-'+str(size-size_1),'[b]')
            SAVED += size - size_1
        if select_file == 2:  # progressive
            os.remove(pathname)
            os.remove(wd+'/'+file_1)
            os.rename(wd+'/'+file_2, pathname)
            print('-'+str(size-size_2),'[p]')
            SAVED += size - size_2
    except BaseException as e:
        print('%s: error while rm & mv' % NAME)
        print(repr(e))
        sys.exit(1)

    return 


NAME = '[smally]'
VER = '%s: compress JPGs losslessly in batch mode and more... V0.11 '\
            'by www.pynote.net' % NAME
JPG = False; PNG = False; GIF = False; WEBP = False
SIZE = 0
SAVED = 0
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--abspath', required=True, 
                        help='absolute path for the picture folder')
    parser.add_argument('--jpg', action='store_true', 
                            help='for both .jpg and .jpeg suffix')
    parser.add_argument('--png', action='store_true')
    parser.add_argument('--gif', action='store_true')
    parser.add_argument('--webp', action='store_true')
    # group for action type
    actType = parser.add_mutually_exclusive_group(required=True)
    actType.add_argument('--show', action='store_true',
                        help='show pathname and size in bytes')
    actType.add_argument('--size', action='store_true',
                        help='calculate total size')
    actType.add_argument('--jpegtran', action='store_true',
                help='lossless compress JPGs with jpegtran tool')
    # version info
    parser.add_argument('-v','--version',action='version',version=VER)
    args = parser.parse_args()  # ~ will be expanded
    # check path
    if (not os.path.isabs(args.abspath) or
        not os.path.exists(args.abspath)):
        print('%s: path must be absolute and existed, support ~' % NAME)
        return
    # check picture type
    global JPG; global PNG; global GIF; global WEBP
    if args.jpg: JPG = True
    if args.png: PNG = True
    if args.gif: GIF = True
    if args.webp: WEBP = True
    if (JPG or PNG or GIF or WEBP) is False:
        print('%s: no picture type choosed' % NAME)
        return
    # actions 
    if args.show: walktree(args.abspath, show_file)
    if args.size:
        walktree(args.abspath, size_file)
        print('%s: total size:'%NAME, str(SIZE)+',',
                str(round(SIZE/1024,2))+'K,',
                str(round(SIZE/1024/1024,3))+'M,',
                str(round(SIZE/1024/1024/1024,4))+'G')
    if args.jpegtran:
        if PNG or GIF or WEBP:
            print('%s: --jpegtran only support JPG' % NAME)
            return
        # which jpegtran
        proc = subprocess.run('which jpegtran',shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        if proc.returncode != 0:
            print('%s: seems jpegtran tool is not there' % NAME)
            print(proc.stderr.decode())
            return
        # which identify
        proc = subprocess.run('which identify',shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        if proc.returncode != 0:
            print('%s: seems identify tool is not there' % NAME)
            print(proc.stderr.decode())
            return
        walktree(args.abspath, jpegtran_jpg)
        print('%s: total saved:'%NAME, str(SAVED)+',',
                str(round(SAVED/1024,2))+'K,',
                str(round(SAVED/1024/1024,3))+'M,',
                str(round(SAVED/1024/1024/1024,4))+'G')

    return


if __name__ == '__main__':
    main()


