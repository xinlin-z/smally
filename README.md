# Contents

* [smally](#smally)
    * [JPG Lossless Compression Algorithm](#JPG-Lossless-Compression-Algorithm)
    * [PNG Lossless Compression](#PNG-Lossless-Compression)
* [How to Install](#How-to-Install)
* [How to Use](#How-to-Use)
    * [Compress JPGs Losslessly in Batch Mode](#Compress-JPGs-Losslessly-in-Batch-Mode)
    * [Get Help](#Get-Help)
    * [Show Pictures' Info](#Show-Pictures-Info)
    * [Show Other Files](#Show-Other-Files)
    * [Calculate Pictures' Total Size](#Calculate-Pictures-Total-Size)
    * [Compress PNG Losslessly in Batch Mode](#Compress-PNG-Losslessly-in-Batch-Mode)
    * [File Mode](#File-Mode)
* [Version](#Version)

# smally

Compress JPG & PNG losslessly in batch mode and more...

The requirements for **smally** is mainly from the picture management and
optimization of website. The core demand for website are faster and faster,
and the core demand for picture are smaller and smaller, and use JPGs as much
as possible for my own opinion.

Smally is highlighted by compressing JPGs losslessly in batch mode, while
choosing the progressive JPG format file whenever it's possible. Besides,
smally also provides a few handy tools to find pictures according to various
parameters.

Smally only use **file extension name** to determine picture type, and skip
all files whose name are started by **-** (dash)!

**中文参考：https://www.pynote.net/archives/882**

## JPG Lossless Compression Algorithm

1. use jpegtran to reduce all metadata in JPG file
2. compare among the original file, baseline format and progressive format
files, choose the smallest one in size
3. whenever possible, choose progressive format version

## PNG Lossless Compression

Simply by calling Optipng to compress PNG. You can feed a compression level
in the command line.

# How to Install

1. You need to make sure **jpegtran**, **identify** and **optipng** can be
found in $PATH
2. You need Python3
3. git clone https://github.com/xinlin-z/smally

Then, you are good to go...

# How to Use

Don't forget **sudo** when you encounter the Permission denied!

## Compress JPGs Losslessly in Batch Mode

Use -p to indicate your picture folder path, which should be one or more
existed paths. -p parameter is mandatory, and use -r to recurse sub folders,
and use -k to keep the compressed file's mtime unchanged.

Use --jpegtran --jpg to compress JPGs losslessly in batch mode.

Example:

    $ python3 smally.py -p path/to/pic -r -k --jpegtran --jpg
    /pics/vim_cheat_sheet.jpg -- [p]
    /pics/firefox_ca_info.jpg -- [p]
    /pics/reset_firefox.jpg -- [p]
    /pics/reset_firefox-400x271.jpg -2246 -9.16% [p]
    /pics/bad_ad.jpg -240 -6.33% [b]
    /pics/dns_jumper-200x92.jpg -704 -9.92% [p]
    /pics/jpg_youhua-400x326.jpg -2987 -11.17% [p]
    /pics/reset_firefox-200x136.jpg -588 -7.25% [p]
    /pics/tplink_dns-200x141.jpg -597 -11.32% [b]
    /pics/vim_cheat_sheet-400x278.jpg -3228 -7.55% [p]
    /pics/dns_test-193x150.jpg -797 -8.27% [p]
    /pics/firefox_privacy-200x49.jpg -400 -12.28% [b]
    /pics/vim_cheat_sheet-200x139.jpg -906 -7.23% [p]
    /pics/bitmap.jpg -- [p]
    /pics/dns_test.jpg -- [p]
    /pics/jpg_youhua.jpg -- [p]
    /pics/firefox_privacy.jpg -- [p]
    /pics/dns_jumper.jpg -- [p]
    /pics/jpg_youhua-184x150.jpg -638 -8.51% [b]
    /pics/dns_test-400x310.jpg -2961 -7.81% [p]
    /pics/firefox_ca_info-400x448.jpg -4038 -8.19% [p]
    /pics/bitmap-200x83.jpg -680 -9.55% [p]
    /pics/tplink_dns.jpg -- [p]
    /pics/001.jpg __Wrong_File_Data_or_Name
    /pics/tplink_dns-768x542.jpg -5194 -13.35% [p]
    /pics/firefox_ca_info-134x150.jpg -479 -6.57% [b]
    /pics/firefox_privacy-400x98.jpg -857 -9.63% [p]
    /pics/tplink_dns-400x282.jpg -1420 -9.49% [p]
    /pics/dns_jumper-400x184.jpg -2355 -10.96% [p]
    [smally]: total saved: 31315, 30.58K, 0.03M, 0.0G, 19/28/1/124


Explain:

Each picture's absolute path will be printed out followed by a few column of
infomation which represents the smally's workout.

**--** : means no change in file size

**-xxx** : means how mang bytes saved

**-xx.xx%** : means how many percentage compressed against original size

**[b]** : means to choose baseline JPG format finally

**[p]** : means to choose progressive JPG format finally

**c/n/e/t** : means there are total t files (all kinds of files) scanned,
          with e of them detected error (file is not picture but with
          a picture extension or file name prefix with -),
          with n of them are called action (show, size, compress) procedure,
          with c of them are really do the action.

In --show and --size actions, c always equals n!

Only show info of compressed if there are too many pictures:

    $ python3 smally.py -p path/to/pic -r -k --jpegtran --jpg | \
            grep -E "\s-[0-9]{1,}\s"

## Get Help

There are many usage examples in help info.

    $ python3 smally.py -h

**-p** option is used to indicate one or more existed paths.

**-i** option is used to add time interval (milliseconds) between each
piture's process. This may be helpful in your busy production server.

**-r** option is used to recurse sub folders. The default behavior is not
recursive.

**-k** option is used to keep the mtime of compressed file unchanged. This
is useful with -t option in case you have a daily routine to compress.

**-t** option is used to set a time window in seconds. Only the files are not
old than the time window compute from now would took action. While --jpegtran,
-k option should be used with -t together.

Pay attention: While jpegtran JPGs in batch mode, the check of time window is
ahead of the check of file itself. So, the e in c/n/e/t info is only the
accumulated number within the time window, and the e+n means all the
candidating file among the t scanned.

## Show Pictures' Info

Use --show to get pictures' info.

Example for showing JPGs' info only:

    $ python3 smally.py -p uploads/2019/01 --show --jpg
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
    [smally]: display stat: 17/17/0/27

Example for showing both JPGs and PNGs recursively:

    $ python3 smally.py -p path/to/pic -r --show --jpg --png

So, there are 4 parameters to indicate picture file type, --jpg, --png, --gif
and --webp. They can be all presented in command line, and must be at least
one to be presented.

You are encouraged to use smally combined with other Linux command line tools,
such as sort, grep...Here are several examples:

Show your Top10 PNG picture in size:

    $ python3 smally.py -p path/to/pic -r --show --png | sort -k3nr | head

Show all your JPGs which are bigger than 1000K:

    $ python3 smally.py -p path/to/pic -r --show --jpg | grep -E \
            "\s[0-9]{4}.*K$"

Show all JPGs whose width is lager than 768 pixel:

    $ python3 smally.py -p path/to/pic -r --show --jpg | grep -E \
            "\s(769|[7-9][7-9][0-9]|[8|9][0-9]{2}|[0-9]{4,})x.*\s"

## Show Other Files

If you don't specify the picture type while using --show command, you'll get
all other files' info.

There are three types of other files, shown as below:

    $ python3 ~/repos/smally/smally.py -p . --show
    /home/pi/test/pics/pkg.link __Not_Reg_File
    /home/pi/test/pics/iamnotapic __Not_Pic_File_Extension

Another type of other files is files with picture extensions, but are not
pictures, or file name with prefix -.

    $ python3 smally.py -p path --show --jpg --gif --png | grep __Wrong_File

## Calculate Pictures' Total Size

Use --size to calculate pictures' total size in the folder you spcefied.

Example for calculating all GIFs and PNGs total size:

    $ python3 smally.py -p path/to/pic -r --size --gif --png
    [smally]: total size: 28099, 27.44K, 0.027M, 0.0G, 5/5/0/5

You can not use smally to get a single picture's size, please use ls -l.

## Compress PNG Losslessly in Batch Mode

    $ python3 smally.py -p path -r -k --optipng o2 --png

The -fix option is joined in the optipng command line, so it is possible
that you find the size is a little bigger after compression. This is the
cost for fixing broken png files.

## File Mode

To use -f option, you can specify files in cmd line:

    $ python3 smally.py -f file1 file2 --show --jpg --png
    $ python3 smally.py -f file1 file2 --size --jpg --png
    $ python3 smally.py -f file1 file2 --jpegtran --jpg
    $ python3 smally.py -f file1 file2 --optipng o2 --png

# Version

* **2021-01-24 V0.23**
    - add -f option, file mode
    - bugfix

* **2020-10-30 V0.22**
    - add --optipng to compress PNGs
    - refactor a little

* **2020-07-05 V0.21**
    - replace print by logging
    - more counting info (l/n/m --> c/n/e/t)
    - show other files' info by --show without picture type
    - update -h info and strip trailing whitespace
    - bugfix

* **2020-03-07 V0.20**
    - change -a to -p, which can take one or more relevant paths now

* **2020-02-06 V0.19**
    - add -r option
    - add -k option
    - add -t option
    - tweak -a option behevior, which can take more than one path

* **2020-01-29 V0.18**
    - refactor code completely into OOP way
    - tweak show info while jpegtran jpg process (n/m --> l/n/m)

* **2019-12-31 V0.17**
    - add -i option
    - restore and delete temporary while exceptions
    - bugfix and code optimization
    - rewrite README.md

* **2019-09-17 V0.16**
    - add percentage info while compressing
    - slightly structure optimization

* **2019-08-30 V0.15**
    - count the number of compressed jpg
    - change several return to sys.exit(1)
    - tweaks

* **2019-08-24 V0.12**
    - add width x height info in show cmd
    - optimize algo
    - update readme.md
    - tweaks and bugfix

* **2019-08-19 V0.09**
    - The first release.


