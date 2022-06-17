# need to run in smally repos folder
set -eu


echo 'test smally.py ...'
cp -r testpic _ttpic
python3 smally.py --jpegtran _ttpic/102.jpg
python3 smally.py --optipng _ttpic/201.png
python3 smally.py --gifsicle _ttpic/302.gif
rm -rf _ttpic 


echo 'test smally.sh ...'
cp -r testpic _ttpic
bash smally.sh _ttpic/102.jpg
bash smally.sh _ttpic/201.png
bash smally.sh _ttpic/302.gif
rm -rf _ttpic 


echo 'test find with smally.sh ...'
cp -r testpic _ttpic
find _ttpic -type f -exec bash smally.sh {} \;
rm -rf _ttpic 


echo 'Test Done!'

