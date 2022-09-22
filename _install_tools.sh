#!/usr/bin/bash
set -e
cd $(dirname $0)/3rdParty
. common.sh


# check $1
if [ -z $1 ]; then
    echo 'error: no parameter (JPEG, PNG or GIF)'
    exit 1
fi


# install_tool <name-version.tar.gz> <bin_name>
function install_tool() {
    local tdir=$(echo $1 | awk -F- '{print $1}')
    local bindir=/usr/local/smally
    mkdir -p $tdir
    tar zxf $1 -C $tdir
    cd $tdir/*
    # gifsicle needs something different
    if [ $2 == 'gifsicle' ]; then
        autoreconf -i
        ./configure --prefix=$bindir/$tdir --disable-gifview --disable-gifdiff
    else
        ./configure --prefix=$bindir/$tdir
    fi
    make && make install
    cd -
    rm -rf $tdir
    rm -f /usr/bin/$2
    ln -s $bindir/$tdir/bin/$2 /usr/bin/$2
}


while [ $1 ]; do
    case $1 in
        JPEG)
            echo "installing $JPEG"
            bash download_tools.sh JPEG
            install_tool $JPEG jpegtran
            ;;
        PNG)
            echo "installing $OPTIPNG"
            bash download_tools.sh PNG
            install_tool $OPTIPNG optipng
            ;;
        GIF)
            echo "installing $GIF"
            bash download_tools.sh GIF
            install_tool $GIF gifsicle
            ;;
        *)
            echo 'error: parameter value should be in (JPEG, PNG or GIF)'
            exit 4
            ;;
    esac
    shift
done

echo 'All Done! ^____^'

