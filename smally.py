#!/usr/bin/env python3 
import os 
import sys
import argparse
from stat import *
import subprocess
import time


# contants
NAME = '[smally]'
VER = '%s: compress JPGs losslessly in batch mode and more... V0.17 '\
            'by www.pynote.net' % NAME
FILE_WRONG = '__Wrong_File_Data_or_Name'


def walktree(top, call):
    """walk file tree from position top, 
    for each file, callback is called."""
    
    def __call(pathname):
        basename = os.path.basename(pathname)
        if identify_cmd(pathname) is False or basename[0] == '-':
            print(pathname + FILE_WRONG)
        else: call(pathname)
        time.sleep(gInterval)  # interval in between
    
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        try: 
            mode = os.stat(pathname, follow_symlinks=False).st_mode
        except:
            continue
        if S_ISDIR(mode):
            walktree(pathname, call)  # directory, recurse into it
        elif S_ISREG(mode) is False:
            continue                  # skip all non-regular file
        else:
            # get file extension
            _, file_ext = os.path.splitext(pathname)
            # call accordingly
            if (file_ext == '.jpg' or file_ext == '.jpeg') and gJPG == True:
                __call(pathname)
                continue
            if file_ext == '.png' and gPNG == True:
                __call(pathname)
                continue
            if file_ext == '.gif' and gGIF == True:
                __call(pathname)
                continue
            if file_ext == '.webp' and gWEBP == True:
                __call(pathname)

    
def _shell_cmd(cmd, cwd=None):
    """execute a shell cmd,
    return returncode, stdout, stderr"""
    proc = subprocess.run(cmd, shell=True, cwd=cwd, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def which_cmd(cmd):
    """use which to check if cmd is in $PATH"""
    cmd_str = 'which %s' % cmd
    rcode, _, err = _shell_cmd(cmd_str)
    if rcode != 0:
        print('%s: %s can not be found in $PATH ' % (NAME,cmd))
        print(err.decode())
        return False
    return True


def identify_cmd(pathname):
    """identify if a file is a legal picture format."""
    rcode, _, _= _shell_cmd('identify %s' % pathname)
    return True if rcode == 0 else False


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
    """show pathname WxH *K accordingly"""
    size = os.path.getsize(pathname)
    print(pathname, getWxH(pathname), str(round(size/1024,2))+'K') 


def size_file(pathname):
    """calculate total size of picture choosed"""
    global gSize
    gSize += os.path.getsize(pathname)


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


def _jpg_wash_floor(pathname, wd, file1, file2):
    """try to restore pathname and delete tmp files while exceptions"""
    if os.path.exists(pathname):
        try: os.remove(wd+'/'+file1)
        except: pass
        try: os.remove(wd+'/'+file2)
        except: pass
    else:
        if (os.path.exists(wd+'/'+file1) and 
            os.path.exists(wd+'/'+file2)):
            size1 = os.path.getsize(wd+'/'+file1)
            size2 = os.path.getsize(wd+'/'+file2)
            if size1 >= size2:
                os.remove(wd+'/'+file1)
                os.rename(wd+'/'+file2, pathname)
            else:
                os.remove(wd+'/'+file2)
                os.rename(wd+'/'+file1, pathname)
        elif os.path.exists(wd+'/'+file2):
            os.rename(wd+'/'+file2, pathname)
        else: os.rename(wd+'/'+file1, pathname)


def jpegtran_jpg(pathname):
    """use jpegtran compress jpg losslessly"""
    global gTotalJpgNum; 
    gTotalJpgNum += 1 
    try:
        basename = os.path.basename(pathname)
        wd = os.path.dirname(pathname)
        # baseline 
        file_1 = '__smally_jpg1_' + basename
        cmd_1 = 'jpegtran -copy none -optimize %s > %s' % (basename,file_1)
        rcode, _, err = _shell_cmd(cmd_1, wd)
        if rcode != 0:
            raise ChildProcessError('%s: error while jpegtran baseline '
                                    'compression\n' % NAME
                                    + err.decode())
        # progressive
        file_2 = '__smally_jpg2_' + basename
        cmd_2 = 'jpegtran -copy none -progressive %s > %s' % (basename,file_2)
        rcode, _, err = _shell_cmd(cmd_2, wd)
        if rcode != 0:
            raise ChildProcessError('%s: error while jpegtran progressive '
                                    'compression\n' % NAME
                                    + err.decode())
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
        print(pathname, end=' ')
        if select_file == 0:  # origin
            os.remove(wd+'/'+file_1)
            os.remove(wd+'/'+file_2)
            if isProgressive(pathname) is True:
                print('-- [p]')
            else: print('-- [b]')
        else: 
            global gCompJpgNum
            gCompJpgNum += 1 
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
    # use BaseException to catch KeyboardInterrupt
    except BaseException as e: 
        print(repr(e))
        # make sure wd, file_1, file_2 are all defined
        if 'wd' not in locals().keys(): sys.exit(1)
        if 'file_1' not in locals().keys(): sys.exit(1)
        if 'file_2' not in locals().keys(): 
            os.remove(wd+'/'+file1)
            sys.exit(1)
        _jpg_wash_floor(pathname, wd, file_1, file_2)
        sys.exit(1)


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
    global gJPG; global gPNG; global gGIF; global gWEBP
    if args.jpg: gJPG = True
    if args.png: gPNG = True
    if args.gif: gGIF = True
    if args.webp: gWEBP = True
    if (gJPG or gPNG or gGIF or gWEBP) is False:
        print('%s: no picture type choosed' % NAME)
        sys.exit(1)
    # interval
    global gInterval
    if args.interval != None:
        if args.interval >= 0: gInterval = args.interval/1000
        else: 
            print('%s: interval time must be positive' % NAME)
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


if __name__ == '__main__':
    # globals
    gJPG = False; gPNG = False; gGIF = False; gWEBP = False
    gSize = 0
    gSaved = 0
    gTotalJpgNum = 0; gCompJpgNum = 0
    gInterval = 0.0;
    main()


