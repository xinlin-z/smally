# need to run in smally repos folder
set -eux

cp -r testpic _ttpic
python3 smally.py --jpegtran _ttpic/102.jpg
python3 smally.py --optipng _ttpic/201.png
python3 smally.py --gifsicle _ttpic/302.gif
rm -rf _ttpic 
