# smally
compress JPGs losslessly in batch mode and more...

The requirements for smally is mainly from the management of website. The core
demand for website is speed, and the core demand for picture is smaller, and
use JPGs as much as possible.

Smally's highligth function is to compress JPGs losslessly in batch mode.
Besides, smally also provides a few handy tools to manage pictures.

for Chinese 中文参考：https://www.pynote.net/archives/882

## how to install smally
1. You need install jpegtran tool
2. You need Python3
3. git clone https://github.com/xinlin-z/smally

## how to use smally

### help info
    $ python3 smally.py -h

### show pictures' info
Show JPGs only:    

    $ python3 smally.py -a ~/path/to/pic --show --jpg

Show Both JPGs and PNGs:
    
    $ python3 smally.py -a ~/path/to/pic --show --jpg --png

Smally show supports 4 picture suffix: --jpg, --png, --gif, --webp.

You are encouraged to use smally combined with other Linux command line tools,
such as sort, grep...Here are several examples:

Show how many JPGs you have:

    $ python3 smally.py -a ~/path/to/pic --show --jpg | wc -l

Show your Top10 PNG picture in size:

    $ python3 smally.py -a ~/path/to/pic --show --png | sort -k2nr | head

Show all your JPGs which are bigger than 1000K:

    $ python3 smally.py -a ~/path/pic --show --jpg | grep -E "\s[0-9]{4}.*K$"

### calculate picture folder's total size
Calculate all JPGs total size:

    $ python3 smally.py -a ~/path/to/pic --size --jpg

Calculate all GIFs and PNGs total size:

    $ python3 smally.py -a ~/path/to/pic --size --gif --png

You can not use smally to get  a single picture's size, please use ls -l.

### compress JPGs losslessly in batch mode
Compress JPGs losslessly in batch mode:

    $ python3 smally.py -a ~/path/to/pic --jpegtran --jpg

## version
* 2019-08-19 V0.09

    The first release.
