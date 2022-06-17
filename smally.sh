#!/usr/bin/bash
set -u


dn=$(dirname $0)
filetype=$(file $1 | awk '{print $2}')

if [ $filetype == 'JPEG' ]; then
    python3 ${dn}/smally.py --jpegtran $1
    exit
fi

if [ $filetype == 'PNG' ]; then
    python3 ${dn}/smally.py --optipng $1
    exit
fi

    
if [ $filetype == 'GIF' ]; then
    python3 ${dn}/smally.py --gifsicle $1
    exit
fi

