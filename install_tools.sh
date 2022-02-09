#!/usr/bin/bash
set -exu


# download tool
which wget
if [ $? -ne 0 ]; then
    which curl
    if [ $? -ne 0 ]; then
        echo 'Both wget and curl are not available, fail and exit...'
        exit 1
    else dtool=curl
    fi
else dtool=wget
fi
echo 'Download tool:' $dtool


# jpegtran
target1=https://www.ijg.org/files/jpegsrc.v9e.tar.gz
t1name=jpeg_v9e.tar.gz
[ -f $t1name ] && 
echo "$t1name is existed..." ||
{
    if [ ${dtool} == 'wget' ]; then opt='-O'; else opt='-o'; fi
    $dtool $target1 $opt $t1name
    if [ $? -ne 0 ]; then
        echo 'Download target1 failed, exit...'
        exit 1
    fi
    unset opt
}

t_dir=jpeg_v9e
mkdir -p $t_dir
tar zxf $t1name -C $t_dir
cd ${t_dir}/jpeg*
./configure --prefix=/usr/local/$t_dir
make && make install
cd -
rm -rf $t_dir
rm -f /usr/bin/jpegtran
ln -s /usr/local/${t_dir}/bin/jpegtran /usr/bin/jpegtran


# optipng
target2=http://nchc.dl.sourceforge.net/project/optipng/OptiPNG/optipng-0.7.7/optipng-0.7.7.tar.gz
t2name=optipng-0.7.7.tar.gz
[ -f $t2name ] && 
echo "$t2name is existed..." ||
{
    if [ ${dtool} == 'wget' ]; then opt='-O'; else opt='-o'; fi
    $dtool $target2 $opt $t2name
    if [ $? -ne 0 ]; then
        echo 'Download target2 failed, exit...'
        exit 1
    fi
    unset opt
}

t_dir=optipng-0.7.7
mkdir -p $t_dir
tar zxf $t2name -C $t_dir
cd ${t_dir}/optipng*
./configure --prefix=/usr/local/$t_dir
make && make install
cd -
rm -rf $t_dir
rm -f /usr/bin/optipng
ln -s /usr/local/${t_dir}/bin/optipng /usr/bin/optipng


# info
echo 'Done! ^____^'

