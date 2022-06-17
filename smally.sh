#!/usr/bin/bash
set -u


dn=$(dirname $0)


file $1 | grep 'JPEG' > /dev/null
if [ $? -eq 0 ]; then
    python3 ${dn}/smally.py --jpegtran $1
    exit
fi


file $1 | grep 'PNG' > /dev/null
if [ $? -eq 0 ]; then
    python3 ${dn}/smally.py --optipng $1
    exit
fi


file $1 | grep 'GIF' > /dev/null
if [ $? -eq 0 ]; then
    python3 ${dn}/smally.py --gifsicle $1
fi
