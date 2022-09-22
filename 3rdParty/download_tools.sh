#!/usr/bin/bash
cd $(dirname $0)
. common.sh


# check $1
if [ -z $1 ]; then
    echo 'error: no parameter (JPEG, PNG or GIF)'
    exit 1
fi


# check and set download tool
which wget > /dev/null 2>&1
if [ $? -ne 0 ]; then
    which curl > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo 'error: no download tool (wget or curl)'
        exit 2
    else
        dtool=curl
        opt='-o'
    fi
else
    dtool=wget
    opt='-O'
fi
echo 'Download Tool:' $dtool


set -e
# download <url> <filename>
function download() {
    [ -f $2 ] &&
    echo "$2 is already existed..." ||
    {
        $dtool $1 $opt $2
        if [ $? -ne 0 ]; then
            echo "Download $2 failed, exit..."
            exit 3
        fi
    }
}


# download
while [ $1 ]; do
    case $1 in
        JPEG)
            echo "downloading $JPEG"
            download $JPEG_URL $JPEG
            ;;
        PNG)
            echo "downloading $OPTIPNG"
            download $OPTIPNG_URL $OPTIPNG
            ;;
        GIF)
            echo "downloading $GIF"
            download $GIF_URL $GIF
            ;;
        *)
            echo 'error: parameter value should be in (JPEG, PNG or GIF)'
            exit 4
            ;;
    esac
    shift
done

echo 'Done!'

