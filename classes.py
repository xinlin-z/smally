#!/usr/bin/env python3
import os
import sys
from stat import *
import time
from datetime import datetime
import subprocess


# contants
NAME = '[smally]'
FILE_WRONG = ' __Wrong_File_Data_or_Name'


class sh():
    """shell command class"""
    @staticmethod
    def cmd(cmd, cwd=None):
        """execute a shell cmd,
        return returncode, stdout, stderr"""
        proc = subprocess.run(cmd, shell=True, cwd=cwd, 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc.returncode, proc.stdout, proc.stderr

    @staticmethod
    def identify(pathname):
        """identify if a file is a legal picture format."""
        rcode, _, _= sh.cmd('identify %s' % pathname)
        return True if rcode == 0 else False

    @staticmethod
    def which(cmd):
        """use which to check if cmd is in $PATH"""
        cmd_str = 'which %s' % cmd
        rcode, _, err = sh.cmd(cmd_str)
        if rcode != 0:
            print('%s: %s can not be found in $PATH ' % (NAME,cmd))
            print(err.decode())
            return False
        return True

    @staticmethod
    def getWxH(pathname):
        """get picture's width x height in pixel"""
        cmd = 'identify %s | cut -d" " -f 3 | head -n1' % pathname
        rcode, out, err = sh.cmd(cmd)
        if rcode != 0:
            print('%s: error while identify jpg width x height' % NAME)
            print(err.decode())
            sys.exit(1)
        wh = out.decode()
        return wh[:len(wh)-1]

    @staticmethod
    def isProgressive(pathname):
        """check if pathname is progressive jpg format"""
        cmd = 'identify -verbose %s | grep Interlace' % pathname
        rcode, out, err = sh.cmd(cmd)
        if rcode != 0:
            print('%s: error while identify jpg format' % NAME)
            print(err.decode())
            sys.exit(1)
        if out.decode().find('None') == -1:  # progressive found
            return True
        return False


class walk(): 
    """Walk tree and callback according to ptype."""
    def __init__(it, ptype, interval, recursive, timewindow):
        it.total = 0            # file number scanned
        it.num_error = 0        # file number error
        it.num_call = 0         # file number processed
        it.num_do = 0           # file number did meaningful action
        it.ptype = ptype
        it.interval = interval
        it.recursive = recursive
        it.now = datetime.now()
        it.tw = timewindow

    def incr_num_do(it):
        """called by subclass action section"""
        it.num_do += 1

    def do(it, pathname):
        pass  # please override in subclass if needed

    def check(it, pathname):
        # check time window
        if it.tw != None: 
            td = it.now - datetime.fromtimestamp(os.path.getmtime(pathname))
            if td.total_seconds() > it.tw: return False
        # check file itself
        if (sh.identify(pathname) is False
              or os.path.basename(pathname)[0] == '-'):
            print(os.path.abspath(pathname) + FILE_WRONG)
            it.num_error += 1
            return False
        return True

    def after(it):
        pass  # please override in subcleass if needed

    def start(it, top):
        for path in top: it.go(path)
        it.after()

    def go(it, top):
        for f in os.listdir(top):
            pathname = os.path.join(top, f)
            try: 
                mode = os.stat(pathname, follow_symlinks=False).st_mode
            except:
                continue
            if S_ISDIR(mode):
                if it.recursive:
                    it.go(pathname)       # directory, recurse into it
                else: continue
            elif S_ISREG(mode) is False:
                continue                  # skip all non-regular file
            else:
                it.total += 1 
                # get file extension
                _, file_ext = os.path.splitext(pathname)
                # call accordingly
                if file_ext in it.ptype: 
                    if it.check(pathname) is False:
                        continue
                    it.do(pathname)
                    it.num_call += 1
                    time.sleep(it.interval)


class pShow(walk):
    """show command"""
    def __init__(it, ptype, interval, recursive, timewindow, path):
        super().__init__(ptype, interval, recursive, timewindow)
        it.start(path)

    def do(it, pathname):
        size = os.path.getsize(pathname)
        print(os.path.abspath(pathname), 
              sh.getWxH(pathname), str(round(size/1024,2))+'K')
        it.incr_num_do()


class pSize(walk):
    """size command"""
    def __init__(it, ptype, interval, recursive, timewindow, path):
        super().__init__(ptype, interval, recursive, timewindow)
        it.size = 0
        it.start(path)

    def after(it):
        print('%s: total size:'%NAME, str(it.size)+',',
                str(round(it.size/1024,2))+'K,',
                str(round(it.size/1024/1024,3))+'M,',
                str(round(it.size/1024/1024/1024,4))+'G')

    def do(it, pathname):
        it.size += os.path.getsize(pathname)
        it.incr_num_do()
        

class pJpegtran(walk):
    """jpegtran command"""
    def __init__(it, ptype, interval, recursive, timewindow, path, keepmtime):
        super().__init__(ptype, interval, recursive, timewindow)
        it.saved = 0
        it.kmt = keepmtime
        it.start(path)

    def after(it):
        print('%s: total saved:'%NAME, str(it.saved)+',',
                str(round(it.saved/1024,2))+'K,',
                str(round(it.saved/1024/1024,3))+'M,',
                str(round(it.saved/1024/1024/1024,4))+'G,',
                str(it.num_do)
                    +'/'+str(it.num_call)
                    +'/'+str(it.num_error)
                    +'/'+str(it.total))
        
    def mtimeStr(it, pathname):
        """get time string can be used by touch -d option"""
        _, out, _ = sh.cmd('stat -c "%y" ' + pathname)
        return out.decode()

    def do(it, pathname):
        try:
            basename = os.path.basename(pathname)
            wd = os.path.dirname(pathname)
            # baseline 
            file_1 = wd + '/'+ '__smally_jpg1_' + basename
            cmd_1 = 'jpegtran -copy none -optimize %s > %s'%(pathname,file_1)
            rcode, _, err = sh.cmd(cmd_1)
            if rcode != 0:
                raise ChildProcessError('%s: error while jpegtran baseline '
                                        'compression\n' % NAME
                                        + err.decode())
            # progressive
            file_2 = wd + '/' + '__smally_jpg2_' + basename
            cmd_2 = 'jpegtran -copy none -progressive %s > %s' \
                    % (pathname,file_2)
            rcode, _, err = sh.cmd(cmd_2)
            if rcode != 0:
                raise ChildProcessError('%s: error while jpegtran progressive '
                                        'compression\n' % NAME
                                        + err.decode())
            # choose the smallest one
            size = os.path.getsize(pathname)
            size_1 = os.path.getsize(file_1)
            size_2 = os.path.getsize(file_2)
            if size <= size_1 and size <= size_2: 
                select_file = 0
                if size == size_2 and sh.isProgressive(pathname) is False: 
                    select_file = 2  # progressive is preferred
            else:
                if size_2 <= size_1: select_file = 2  
                else: select_file = 1
            # rm & mv
            print(os.path.abspath(pathname), end=' ')
            if select_file == 0:  # origin
                os.remove(file_1)
                os.remove(file_2)
                if sh.isProgressive(pathname) is True: print('-- [p]')
                else: print('-- [b]')
            else: 
                it.incr_num_do()
                if it.kmt: mtime = it.mtimeStr(pathname)
            if select_file == 1:  # baseline
                os.remove(pathname)
                os.remove(file_2)
                os.rename(file_1, pathname)
                if it.kmt: sh.cmd('touch -m -d "'+mtime+'" '+pathname)
                saved = size - size_1
                print('-'+str(saved),'-'+str(round(saved/size*100,2))
                         +'%','[b]')
                it.saved += saved
            if select_file == 2:  # progressive
                os.remove(pathname)
                os.remove(file_1)
                os.rename(file_2, pathname)
                if it.kmt: sh.cmd('touch -m -d "'+mtime+'" '+pathname)
                saved = size - size_2
                print('-'+str(saved),'-'+str(round(saved/size*100,2))
                         +'%','[p]')
                it.saved += saved
        # use BaseException to catch KeyboardInterrupt
        except BaseException as e: 
            print(repr(e))
            # wash the floor, make sure delete pathname first in above code
            if os.path.exists(pathname):
                try: os.remove(file_1)
                except: pass
                try: os.remove(file_2)
                except: pass
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
            sys.exit(1)


