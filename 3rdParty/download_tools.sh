#!/usr/bin/bash
set -u
cd $(dirname $0)
. common.sh


# download tool
which wget > /dev/null 2>&1
if [ $? -ne 0 ]; then
    which curl > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo 'Both wget and curl are not available, fail and exit...'
        exit 1
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
            exit 2
        fi
    }
}


echo "downloading $JPEG"
download $JPEG_URL $JPEG
echo "downloading $OPTIPNG"
download $OPTIPNG_URL $OPTIPNG
echo "downloading $GIF"
download $GIF_URL $GIF


echo 'Done!'

