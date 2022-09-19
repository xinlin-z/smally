#!/usr/bin/bash
set -eu
cd $(dirname $0)/3rdParty
bash download_tools.sh
. common.sh


# install_tool <name-version.tar.gz> <bin_name>
function install_tool() {
    local tdir=$(echo $1 | awk -F- '{print $1}')
    mkdir -p $tdir
    tar zxf $1 -C $tdir
    cd $tdir/*
    # gifsicle needs something different
    if [ $2 == 'gifsicle' ]; then
        autoreconf -i
        ./configure --prefix=/usr/local/$tdir --disable-gifview --disable-gifdiff
    else
        ./configure --prefix=/usr/local/$tdir
    fi
    make && make install
    cd -
    rm -rf $tdir
    rm -f /usr/bin/$2
    ln -s /usr/local/$tdir/bin/$2 /usr/bin/$2
}


echo "installing $JPEG"
install_tool $JPEG jpegtran
echo "installing $OPTIPNG"
install_tool $OPTIPNG optipng
echo "installing $GIF"
install_tool $GIF gifsicle


echo 'All Done! ^____^'

