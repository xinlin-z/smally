#!/usr/bin/bash
set -u
cd $(dirname $0)


function check_tool(){
    which $1 > /dev/null
    if [ $? -ne 0 ]; then
        echo $1 not found
        exit 1
    fi
    echo found $1
}


check_tool jpegtran
check_tool optipng
check_tool gifsicle


echo '# Test smally.py with type'
cp -r testpic _ttpic
python3 smally.py -j _ttpic/102.jpg
python3 smally.py -p _ttpic/201.png
python3 smally.py -g _ttpic/302.gif
rm -rf _ttpic

echo '# Test smally.py with single file'
cp -r testpic _ttpic
python3 smally.py _ttpic/102.jpg
python3 smally.py _ttpic/201.png
python3 smally.py _ttpic/302.gif
rm -rf _ttpic

echo '# Test smally.py with directory'
cp -r testpic _ttpic
cp -r testpic _ttpic/
python3 smally.py -r _ttpic -P4
rm -rf _ttpic


echo 'Test OK!'

