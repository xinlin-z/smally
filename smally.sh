#!/usr/bin/bash
#######################################
# Useage:
# $ bash smally.sh [-t type] <filename>
#######################################


if [ $1 == '-t' ]; then
    case $2 in
        JPEG|PNG|GIF)
            opt=$2
            ;;
        *)
            echo 'option -t type error (JPEG, PNG or GIF)'
            exit 1
            ;;
    esac
    shift
    shift
fi


dn=$(dirname $0)
ftype=$(file $1 | awk '{print $2}')


case $ftype in
    JPEG)
        if [ -z $opt ] || [ $opt == 'JPEG' ]; then
            python3 ${dn}/smally.py --jpegtran $1
        fi
        ;;
    PNG)
        if [ -z $opt ] || [ $opt == 'PNG' ]; then
            python3 ${dn}/smally.py --optipng $1
        fi
        ;;
    GIF)
        if [ -z $opt ] || [ $opt == 'GIF' ]; then
            python3 ${dn}/smally.py --gifsicle $1
        fi
        ;;
esac

