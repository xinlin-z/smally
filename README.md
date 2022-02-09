* [Smally](#Smally)
    * [JPEG Compression](#JPEG-Compression)
    * [PNG Compression](#PNG-Compression)
    * [Install](#Install)
    * [Run Test](#Run-Test)
    * [Usage](#Usage)
    * [Screenshot](#Screenshot)
    * [Old Version](#Old-Version)

# Smally

A simple tool to compress all JPEG and PNG files losslessly in a folder, by
invoking the famous jpegtran and optipng.

Smally uses `file` to determine if it is a JPEG or PNG, and it would keep
the file name and mtime unchnaged after compression!

## JPEG Compression

1. Using jpegtran to reduce all metadata.
2. To compare among the original file, baseline format and progressive format
files, choose the smallest one in size.
3. Whenever possible, choose progressive format version.

## PNG Compression

Simply calling optipng to compress PNG, in the most crazy level.

## Install

``` shell
$ git clone https://github.com/xinlin-z/smally
$ cd smally
$ sudo bash install_tools.sh
```

This will setup the latest version jpegtran and optipng in /usr/bin
automatically.

##  Run Test

``` shell
$ bash test.sh
```

##  Usage

Normally:

``` shell
$ find <path/to/image_folder> -type f -exec bash smally.sh {} \;
```

For single file:

``` shell
$ python3 smally.py --jpegtran <jpeg_file>
$ python3 smally.py --optipng <png_file>
```

For single file which you don't know format:

``` shell
$ bash smally.sh <filename>
```

## Screenshot

![smally](/screenshot.png)

## Old Version

This version (from V0.50) of smally is a total refactor one, old versions
are too complicated, which I do not recommend!

