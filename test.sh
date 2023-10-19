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

echo '# Test smally.py without ftype'
cp -r testpic _ttpic
python3 smally.py _ttpic/102.jpg
python3 smally.py _ttpic/201.png
python3 smally.py _ttpic/302.gif
rm -rf _ttpic

echo '# Test smally.py with directory'
cp -r testpic _ttpic
python3 smally.py _ttpic
rm -rf _ttpic

echo '# Test smally.sh'
cp -r testpic _ttpic
bash smally.sh _ttpic/102.jpg
bash smally.sh _ttpic/201.png
bash smally.sh _ttpic/302.gif
rm -rf _ttpic


function run_with_wrong_type(){
    bash smally.sh -t ABCD $1 > /dev/null
    if [ $? -ne 1 ]; then
        echo 'exit code is not expected'
        rm -rf _ttpic
        exit 1
    fi
}


echo '# Test smally.sh -t'
cp -r testpic _ttpic
bash smally.sh -t JPEG _ttpic/102.jpg
bash smally.sh -t PNG _ttpic/201.png
bash smally.sh -t GIF _ttpic/302.gif
run_with_wrong_type _ttpic/102.jpg
run_with_wrong_type _ttpic/201.png
run_with_wrong_type _ttpic/302.gif
rm -rf _ttpic


echo '# Test find with smally.sh'
cp -r testpic _ttpic
find _ttpic -type f -exec bash smally.sh {} \;
rm -rf _ttpic


echo '# Test find with smally.sh -t'
cp -r testpic _ttpic
find _ttpic -type f -exec bash smally.sh -t JPEG {} \;
find _ttpic -type f -exec bash smally.sh -t PNG {} \;
find _ttpic -type f -exec bash smally.sh -t GIF {} \;
rm -rf _ttpic


echo 'Test OK!'

