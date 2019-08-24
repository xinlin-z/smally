# smally
compress JPGs losslessly in batch mode and more...

The requirements for smally is mainly from the picture management and 
optimization of website. The core requirement for website is speed, and the 
core requirement for picture is smaller, and use JPGs as much as possible.

Smally's highlight feature is to compress JPGs losslessly in batch mode, while
choose progressive format file when it's possible. Besides, smally provides a 
few handy tools to manage pictures for webmaster.

For Chinese 中文参考：https://www.pynote.net/archives/882

## how to install
1. You need to make sure *jpegtran* and *identify* can be found in $PATH
2. You need Python3
3. git clone https://github.com/xinlin-z/smally
4. Good to go ...

## how to use
### get help
    $ python3 smally.py -h

### show pictures' info
Show JPGs' info only:    

    $ python3 smally.py -a ~/path/to/pic --show --jpg

Show Both JPGs and PNGs:
    
    $ python3 smally.py -a ~/path/to/pic --show --jpg --png

Smally show feature supports 4 picture suffix: --jpg, --png, --gif, --webp.

You are encouraged to use smally combined with other Linux command line tools,
such as sort, grep...Here are several examples:

Show how many JPGs you have:

    $ python3 smally.py -a ~/path/to/pic --show --jpg | wc -l

Show your Top10 PNG picture in size:

    $ python3 smally.py -a ~/path/to/pic --show --png | sort -k2nr | head

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
    /home/pynote.net/pic/uploads/2019/06/wepy-200x103.jpg -523 [p]
    /home/pynote.net/pic/uploads/2019/06/use_python.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/06/use_python-400x432.jpg -892 [b]
    /home/pynote.net/pic/uploads/2019/06/python-logo-400x140.jpg -753 [b]
    /home/pynote.net/pic/uploads/2019/06/tim_peters-400x351.jpg -1121 [p]
    /home/pynote.net/pic/uploads/2019/06/guido_van_rossum.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/06/rot13.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/06/tim_peters.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/06/python_logo.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/06/import_this-400x405.jpg -1006 [b]
    /home/pynote.net/pic/uploads/2019/06/import_this.jpg -- [b]
    /home/pynote.net/pic/uploads/2019/06/python_logo-200x56.jpg -689 [p]
    /home/pynote.net/pic/uploads/2019/06/use_python-139x150.jpg -406 [b]
    /home/pynote.net/pic/uploads/2019/06/wepy.jpg -489 [p]
    /home/pynote.net/pic/uploads/2019/06/rot13-400x243.jpg -2561 [p]
    /home/pynote.net/pic/uploads/2019/06/tim_peters-171x150.jpg -434 [p]
    /home/pynote.net/pic/uploads/2019/06/import_this-148x150.jpg -476 [b]
    /home/pynote.net/pic/uploads/2019/06/python-logo-200x70.jpg -420 [b]
    /home/pynote.net/pic/uploads/2019/06/rot13-200x122.jpg -755 [p]
    /home/pynote.net/pic/uploads/2019/06/guido_van_rossum-200x134.jpg -426 [p]
    /home/pynote.net/pic/uploads/2019/06/python-logo.jpg -174 [b]
    /home/pynote.net/pic/uploads/2019/06/python_logo-400x112.jpg -1499 [p]
    /home/pynote.net/pic/uploads/2019/08/xlrd_test_xls-200x108.jpg -581 [b]
    /home/pynote.net/pic/uploads/2019/08/xlrd_test_xls-400x217.jpg -2003 [p]
    /home/pynote.net/pic/uploads/2019/08/liang.jpg -492 [p]
    /home/pynote.net/pic/uploads/2019/08/email_reply_to-400x600.jpg -5364 [p]
    /home/pynote.net/pic/uploads/2019/08/ren-200x140.jpg -469 [p]
    /home/pynote.net/pic/uploads/2019/08/merged_cells.jpg -143 [b]
    /home/pynote.net/pic/uploads/2019/08/liang-200x128.jpg -391 [b]
    /home/pynote.net/pic/uploads/2019/08/email_reply_to-100x150.jpg -480 [b]
    /home/pynote.net/pic/uploads/2019/08/ren.jpg -1640 [p]
    /home/pynote.net/pic/uploads/2019/08/email_reply_to.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/08/xlrd_test_xls.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/08/merged_cells-200x112.jpg -603 [b]
    /home/pynote.net/pic/uploads/2019/08/flower.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/08/picture.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/08/email_html.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/08/email_html-169x150.jpg -577 [p]
    /home/pynote.net/pic/uploads/2019/08/email_html-400x356.jpg -2276 [p]
    /home/pynote.net/pic/uploads/2019/08/email_plain.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/08/email_plain-200x135.jpg -892 [b]
    /home/pynote.net/pic/uploads/2019/08/email_plain-400x269.jpg -2088 [p]
    /home/pynote.net/pic/uploads/2019/07/dotpy-150x150.jpg -709 [b]
    /home/pynote.net/pic/uploads/2019/07/python-logo5-200x65.jpg -471 [b]
    /home/pynote.net/pic/uploads/2019/07/email_diff_mime-71x150.jpg -387 [b]
    /home/pynote.net/pic/uploads/2019/07/email_jpg_attach-400x492.jpg -2184 [p]
    /home/pynote.net/pic/uploads/2019/07/python-logo5.jpg -146 [b]
    /home/pynote.net/pic/uploads/2019/07/python_code-200x100.jpg -573 [p]
    /home/pynote.net/pic/uploads/2019/07/metro-200x133.jpg -843 [p]
    /home/pynote.net/pic/uploads/2019/07/email_addr.jpg -- [b]
    /home/pynote.net/pic/uploads/2019/07/two_jpg_email-400x589.jpg -3053 [p]
    /home/pynote.net/pic/uploads/2019/07/email_name_addr-200x41.jpg -536 [b]
    /home/pynote.net/pic/uploads/2019/07/two_jpg_email-102x150.jpg -400 [b]
    /home/pynote.net/pic/uploads/2019/07/dotpy.jpg -962 [b]
    /home/pynote.net/pic/uploads/2019/07/email_name_addr.jpg -6 [b]
    /home/pynote.net/pic/uploads/2019/07/email.jpg -- [b]
    /home/pynote.net/pic/uploads/2019/07/email_jpg_attach.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/07/two_jpg_email.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/07/email_pic-114x150.jpg -426 [b]
    /home/pynote.net/pic/uploads/2019/07/email_addr-200x102.jpg -517 [p]
    /home/pynote.net/pic/uploads/2019/07/email_diff_mime-400x840.jpg -4214 [p]
    /home/pynote.net/pic/uploads/2019/07/email_pic.jpg -- [p]
    /home/pynote.net/pic/uploads/2019/07/email_jpg_attach-122x150.jpg -448 [b]
    /home/pynote.net/pic/uploads/2019/07/python_code.jpg -- [b]
    /home/pynote.net/pic/uploads/2019/07/metro.jpg -1348 [p]
    /home/pynote.net/pic/uploads/2019/07/email_diff_mime.jpg -- [p]
    /home/pynote.net/pic/goTop.jpg -339 [b]
    /home/pynote.net/pic/404.jpg -- [p]
    /home/pynote.net/pic/logo.jpg -727 [p]
    [smally]: total saved: 48912, 47.77K, 0.047M, 0.0G

## version
* 2019-08-24 V0.12

    1. add width x height info in show cmd
    2. optimize algo
    3. update readme.md
    4. tweaks and bugfix

* 2019-08-19 V0.09

    The first release.
