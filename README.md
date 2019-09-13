# smally
compress JPG losslessly in batch mode and more...

The requirements for smally is mainly from the picture management and 
optimization of website. The core requirement for website is speed, and the 
core requirement for picture is smaller, and use JPGs as much as possible.

Smally's highlight feature is to compress JPGs losslessly in batch mode, while
choose progressive format file when it's possible. Besides, smally provides a 
few handy tools to manage pictures for webmaster.

**For Chinese 中文参考：https://www.pynote.net/archives/882**

## JPG lossless compression algorithm
1. use jpegtran to reduce all metadata in JPG file
2. compare the original file, baseline format and progressive format file,
choose the smallest one
3. when possible, choose progressive format version

## how to install
1. You need to make sure **jpegtran** and **identify** can be found in $PATH
2. You need Python3
3. git clone https://github.com/xinlin-z/smally

Then, you are good to go ...

## how to use
### get help
    $ python3 smally.py -h

### show pictures' info
Show JPGs' info only:    

    $ python3 smally.py -a ~/path/to/pic --show --jpg
    /home/pic/uploads/2019/01/ieee754-2008-400x224.jpg 400x224 18.37K
    /home/pic/uploads/2019/01/stepstone-768x512.jpg 768x512 94.33K
    /home/pic/uploads/2019/01/ieee754-2008-200x112.jpg 200x112 6.29K
    /home/pic/uploads/2019/01/stepstone.jpg 1000x667 119.69K
    /home/pic/uploads/2019/01/heshu.jpg 500x314 40.68K
    /home/pic/uploads/2019/01/ieee754-2008.jpg 593x332 34.62K
    /home/pic/uploads/2019/01/git.jpg 200x150 6.4K
    /home/pic/uploads/2019/01/stepstone-200x133.jpg 200x133 11.09K
    /home/pic/uploads/2019/01/zhangdie.jpg 490x854 67.49K
    /home/pic/uploads/2019/01/heshu-200x126.jpg 200x126 10.73K
    /home/pic/uploads/2019/01/zhangdie-400x697.jpg 400x697 43.32K
    /home/pic/uploads/2019/01/juanji-400x257.jpg 400x257 15.08K
    /home/pic/uploads/2019/01/zhangdie-86x150.jpg 86x150 3.97K
    /home/pic/uploads/2019/01/heshu-400x251.jpg 400x251 29.86K
    /home/pic/uploads/2019/01/stepstone-400x267.jpg 400x267 34.39K
    /home/pic/uploads/2019/01/juanji.jpg 662x426 27.96K
    /home/pic/uploads/2019/01/juanji-200x129.jpg 200x129 6.26K


Show Both JPGs and PNGs:
    
    $ python3 smally.py -a ~/path/to/pic --show --jpg --png

Smally show feature supports 4 picture suffix: --jpg, --png, --gif, --webp.

You are encouraged to use smally combined with other Linux command line tools,
such as sort, grep...Here are several examples:

Show how many JPGs you have:

    $ python3 smally.py -a ~/path/to/pic --show --jpg | wc -l

Show your Top10 PNG picture in size:

    $ python3 smally.py -a ~/path/to/pic --show --png | sort -k3nr | head

Show all your JPGs which are bigger than 1000K:

    $ python3 smally.py -a ~/path/pic --show --jpg | grep -E "\s[0-9]{4}.*K$"

Show all JPGs whose width is lager than 768 pixel:

    $ python3 smally.py -a ~/path/to/pic --show --jpg | grep -E \
            "\s(769|[7-9][7-9][0-9]|[8|9][0-9]{2}|[0-9]{4,})x.*\s"

### calculate picture's total size in specific folder
Calculate all GIFs and PNGs total size:

    $ python3 smally.py -a ~/path/to/pic --size --gif --png

You can not use smally to get a single picture's size, please use ls -l.

### compress JPGs losslessly in batch mode
Compress JPGs losslessly in batch mode:

    $ python3 smally.py -a ~/path/to/pic --jpegtran --jpg
    /home/pic/uploads/2019/01/ieee754-2008-400x224.jpg -2040 [p]
    /home/pic/uploads/2019/01/stepstone-768x512.jpg -6058 [p]
    /home/pic/uploads/2019/01/ieee754-2008-200x112.jpg -713 [b]
    /home/pic/uploads/2019/01/stepstone.jpg -2818 [p]
    /home/pic/uploads/2019/01/heshu.jpg -5562 [p]
    /home/pic/uploads/2019/01/ieee754-2008.jpg -4737 [p]
    /home/pic/uploads/2019/01/git.jpg -729 [b]
    /home/pic/uploads/2019/01/stepstone-200x133.jpg -952 [p]
    /home/pic/uploads/2019/01/zhangdie.jpg -6114 [p]
    /home/pic/uploads/2019/01/heshu-200x126.jpg -989 [p]
    /home/pic/uploads/2019/01/zhangdie-400x697.jpg -3855 [p]
    /home/pic/uploads/2019/01/juanji-400x257.jpg -1866 [p]
    /home/pic/uploads/2019/01/zhangdie-86x150.jpg -412 [b]
    /home/pic/uploads/2019/01/heshu-400x251.jpg -3515 [p]
    /home/pic/uploads/2019/01/stepstone-400x267.jpg -2702 [p]
    /home/pic/uploads/2019/01/juanji.jpg -3764 [p]
    /home/pic/uploads/2019/01/juanji-200x129.jpg -691 [b]
    [smally]: total saved: 47517, 46.4K, 0.045M, 0.0G, 17/17


**--** means no change

**-xxx** means how mang bytes saved

**[b]** means to choose baseline JPG format finally

**[p]** means to choose progressive JPG format finally

n/m means there are total m pictures and n of them are just compressed 

Only show info of compressed:

    $ python3 smally.py -a ~/path/to/pic --jpegtran --jpg | \
            grep -E "\s-[0-9]{1,}\s"


## version

* **2019-08-30 V0.15**

    1. count the number of compressed jpg
    2. change several return to sys.exit(1)
    3. tweaks

* **2019-08-24 V0.12**

    1. add width x height info in show cmd
    2. optimize algo
    3. update readme.md
    4. tweaks and bugfix

* **2019-08-19 V0.09**

    The first release.
