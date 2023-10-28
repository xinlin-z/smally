* [How to Compress](#How-to-Compress)
    * [JPEG](#JPEG)
    * [PNG](#PNG)
    * [GIF](#GIF)
* [How to Install](#How-to-Install)
* [How to Use](#How-to-Use)
* [APIs](#APIs)
* [Showcase](#Showcase)

Smally is a simple tool to compress JPEG, PNG and GIF files losslessly,
by invoking the famous `jpegtran`, `optipng` and `gifsicle` tools,
in batch mode, in-place and keep mtime unchanged. It is written
in Python, but heavily rely on shell.

## How to Compress

### JPEG

1. Using `jpegtran` to remove all metadata, create a baseline version
and a progressive version.
2. To compare among the original file, baseline and progressive
files, choose the smallest one in size.
3. Whenever possible, choose progressive version.

### PNG

Calling `optipng` to compress PNG, in the most crazy `-o7 -zm1-9` level.

### GIF

Calling `gifsicle` to compress GIF, by using `-O3 --color 256`.

## How to Install

```shell
# install tools on Fedora
$ sudo dnf install libjpeg-turbo-utils optipng gifsicle
# install tools on Ubuntu
$ sudo apt install libjpeg-turbo-progs optipng gifsicle
# install smally
$ pip install smally
```

## How to Use

```shell
# inline help
$ python -m smally -h
# to compress a single file, if option is not presented,
# smally will use file command to get file type info.
$ python -m smally [-j|-p|-g] <pathname>
# to compress a directory
$ python -m smally -r -P<N> <pathname>
# to compress all png file in a directory
$ python -m smally -r -P<N> -p <pathname>
```

`-r`, recursively, it's a command line convention and normally you should
use it when deal with a directory.

`-P<N>`, parallel process number, if it is missing, the logical cpu
count number will be used.

## APIs

4 APIs provided by smally:

```python
# import
from smally import (jpegtran,
                    optipng,
                    gifsicle,
                    is_jpeg_progressive)
# signature
def jpegtran(pathname: str) -> tuple[int,int]: ...
def optipng(pathname: str) -> tuple[int,int]: ...
def gifsicle(pathname: str) -> tuple[int,int]: ...
def is_jpeg_progressive(pathname: str) -> bool: ...
```

The first int in returned tuple is the byte number saved. It could be zero,
which means no save. The second int is the original file size.

## Showcase

```shell
$ python -m smally -r tt -P8
# parallel process number:  8
tt/102.jpg -24157 -16.38% [p]
tt/302.gif -333056 -19.67%
tt/201.png -548 -26.37%
```

