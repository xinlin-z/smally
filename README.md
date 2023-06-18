* [Smally](#Smally)
    * [JPEG Compression](#JPEG-Compression)
    * [PNG Compression](#PNG-Compression)
    * [GIF Compression](#GIF-Compression)
    * [Install Tools](#Install-Tools)
        * [Fedora](#Fedora)
        * [Ubuntu](#Ubuntu)
    * [Run Test](#Run-Test)
    * [Usage](#Usage)
    * [API](#API)
    * [Screenshot](#Screenshot)
    * [Old Version](#Old-Version)

# Smally

A simple tool to compress all JPEG, PNG and GIF files losslessly in a folder,
by invoking the famous `jpegtran`, `optipng` and `gifsicle`.

Smally uses `file` command to determine file type, and it would keep
the file name and mtime unchnaged after compression!

## JPEG Compression

1. Using jpegtran to reduce all metadata.
2. To compare among the original file, baseline format and progressive format
files, choose the smallest one in size.
3. Whenever possible, choose progressive format version.

## PNG Compression

Simply calling optipng to compress PNG, in the most crazy `-o7 -zm1-9` level.

## GIF Compression

Simple calling gifsicle to compress GIF, by using `-O3 --color 256`.

## Install Tools

Smally needs `jpegtran`, `optipng` and `gifsicle` to do it's job.

### Fedora

``` shell
$ sudo dnf install libjpeg-turbo-utils optipng gifsicle
```

### Ubuntu

``` shell
sudo apt install libjpeg-turbo-progs optipng gifsicle
```

## Run Test

``` shell
$ bash test.sh
```

This test.sh script will check all needed tools, and run smally on
pictures in testpic.

## Usage

Normally:

``` shell
$ # for all jpeg, png and gif
$ find <path/to/image_folder> -type f -exec bash smally.sh {} \;
$ # only jpeg
$ find <path/to/image_folder> -type f -exec bash smally.sh -t JPEG {} \;
$ # only png
$ find <path/to/image_folder> -type f -exec bash smally.sh -t PNG {} \;
$ # only gif
$ find <path/to/image_folder> -type f -exec bash smally.sh -t GIF {} \;
```

Or to use `xargs' -P parameter` to take advantage of multi-core CPU:

``` shell
$ # -P4 means 4 paralleled processes
$ find <pathname> -type f -print0 | xargs -0 -P4 -I{} bash smally.sh {}
```

For single file:

``` shell
$ python3 smally.py --jpegtran <jpeg_file>
$ python3 smally.py --optipng <png_file>
$ python3 smally.py --gifsicle <gif_file>
```

For single file which you don't know the format:

``` shell
$ bash smally.sh <filename>
```

## API

There are 4 interfaces provided by smally:

```python
from smally import (jpegtran,
                    optipng,
                    gifsicle,
                    is_jpeg_progressive)
```

The first 3 interfaces take a pathname as parameter, and return a tuple
with saved size and the original size. The last one interface also takes
a pathname as parameter, and simply return true or false.

## Screenshot

![smally](/screenshot.png)

## Old Version

This version (from V0.50) of smally is a total refactor one, old versions
are too complicated, which I do not recommend!

