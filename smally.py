#!/usr/bin/env python3 
import os 
import sys
import argparse
from stat import *
import subprocess


# contants
NAME = '[smally]'
VER = '%s: compress JPGs losslessly in batch mode and more... V0.15 '\
            'by www.pynote.net' % NAME


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
            if (file_ext == '.jpg' or file_ext == '.jpeg') and gJPG == True:
                call(pathname)
            if file_ext == '.png' and gPNG == True:
                call(pathname)
            if file_ext == '.gif' and gGIF == True:
                call(pathname)
            if file_ext == '.webp' and gWEBP == True:
                call(pathname)
    return

    
def _shell_cmd(cmd, cwd=None):
    """execute a shell cmd,
    return returncode, stdout, stderr"""
    proc = subprocess.run(cmd, shell=True, cwd=cwd, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def getWxH(pathname):
    """get picture's width x height in pixel"""
    cmd = 'identify %s | cut -d" " -f 3 | head -n1' % pathname
    rcode, out, err = _shell_cmd(cmd)
    if rcode != 0:
        print('%s: error while identify jpg width x height' % NAME)
        print(err.decode())
        sys.exit(1)
    wh = out.decode()
    return wh[:len(wh)-1]


def show_file(pathname):
    """show pathname accordingly"""
    size = os.path.getsize(pathname)
    print(pathname, getWxH(pathname), str(round(size/1024,2))+'K') 
    return


def size_file(pathname):
    """calculate total size of picture choosed"""
    global gSize
    gSize += os.path.getsize(pathname)
    return


def isProgressive(pathname):
    """check if pathname is progressive jpg format"""
    cmd = 'identify -verbose %s | grep Interlace' % pathname
    rcode, out, err = _shell_cmd(cmd)
    if rcode != 0:
        print('%s: error while identify jpg format' % NAME)
        print(err.decode())
        sys.exit(1)
    if out.decode().find('None') == -1:  # progressive found
        return True
    return False


def jpegtran_jpg(pathname):
    """use jpegtran compress jpg losslessly"""
    print(pathname, end=' ')
    global gTotalJpgNum; gTotalJpgNum += 1 
    basename = os.path.basename(pathname)
    if basename[0] == '-':
        print('skip due to file name')
        return
    wd = os.path.dirname(pathname)
    # baseline 
    file_1 = '_1_' + basename
    cmd_1 = 'jpegtran -copy none -optimize %s > %s' % (basename,file_1)
    rcode, _, err = _shell_cmd(cmd_1, wd)
    if rcode != 0:
        print('%s: error while jpegtran baseline compression' % NAME)
        print(err.decode())
        os.remove(wd+'/'+file_1)
        sys.exit(1)
    # progressive
    file_2 = '_2_' + basename
    cmd_2 = 'jpegtran -copy none -progressive %s > %s' % (basename,file_2)
    rcode, _, err = _shell_cmd(cmd_2, wd)
    if rcode != 0:
        print('%s: error while jpegtran progressive compression' % NAME)
        print(err.decode())
        os.remove(wd+'/'+file_2)
        os.remove(wd+'/'+file_1)  # delete temp file_1
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
    global gSaved
    try:
        if select_file == 0:  # origin
            os.remove(wd+'/'+file_1)
            os.remove(wd+'/'+file_2)
            if isProgressive(pathname) is True:
                print('-- [p]')
            else: print('-- [b]')
        else: global gCompJpgNum; gCompJpgNum += 1 
        if select_file == 1:  # baseline
            os.remove(pathname)
            os.remove(wd+'/'+file_2)
            os.rename(wd+'/'+file_1, pathname)
            saved = size - size_1
            print('-'+str(saved),'-'+str(round(saved/size*100,2))+'%','[b]')
            gSaved += saved
        if select_file == 2:  # progressive
            os.remove(pathname)
            os.remove(wd+'/'+file_1)
            os.rename(wd+'/'+file_2, pathname)
            saved = size - size_2
            print('-'+str(saved),'-'+str(round(saved/size*100,2))+'%','[p]')
            gSaved += saved
    except BaseException as e:
        print('%s: error while rm & mv' % NAME)
        print(repr(e))
        sys.exit(1)

    return 


def which_cmd(cmd):
    """use which to check if cmd is in $PATH"""
    cmd_str = 'which %s' % cmd
    rcode, _, err = _shell_cmd(cmd_str)
    if rcode != 0:
        print('%s: %s can not find in $PATH ' % (NAME,cmd))
        print(err.decode())
        return False
    return True


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
                        help='show pathname and size in KB')
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
        sys.exit(1)
    # check picture type
    global gJPG; global gPNG; global gGIF; global gWEBP
    if args.jpg: gJPG = True
    if args.png: gPNG = True
    if args.gif: gGIF = True
    if args.webp: gWEBP = True
    if (gJPG or gPNG or gGIF or gWEBP) is False:
        print('%s: no picture type choosed' % NAME)
        sys.exit(1)
    # actions 
    if args.show: 
        if which_cmd('identify') is False: sys.exit(1) 
        walktree(args.abspath, show_file)
    if args.size:
        walktree(args.abspath, size_file)
        print('%s: total size:'%NAME, str(gSize)+',',
                str(round(gSize/1024,2))+'K,',
                str(round(gSize/1024/1024,3))+'M,',
                str(round(gSize/1024/1024/1024,4))+'G')
    if args.jpegtran:
        if gPNG or gGIF or gWEBP:
            print('%s: --jpegtran only support JPG' % NAME)
            sys.exit(1)
        if which_cmd('jpegtran') is False: sys.exit(1)
        if which_cmd('identify') is False: sys.exit(1)
        walktree(args.abspath, jpegtran_jpg)
        print('%s: total saved:'%NAME, str(gSaved)+',',
                str(round(gSaved/1024,2))+'K,',
                str(round(gSaved/1024/1024,3))+'M,',
                str(round(gSaved/1024/1024/1024,4))+'G,',
                str(gCompJpgNum)+'/'+str(gTotalJpgNum))

    return


if __name__ == '__main__':
    # globals
    gJPG = False; gPNG = False; gGIF = False; gWEBP = False
    gSize = 0
    gSaved = 0
    gTotalJpgNum = 0; gCompJpgNum = 0
    main()


