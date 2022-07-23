#!/usr/bin/bash
set -u


dn=$(dirname $0)
filetype=$(file $1 | awk '{print $2}')

case $filetype in
    JPEG) python3 ${dn}/smally.py --jpegtran $1;;
    PNG)  python3 ${dn}/smally.py --optipng $1;;
    GIF)  python3 ${dn}/smally.py --gifsicle $1;;
esac

