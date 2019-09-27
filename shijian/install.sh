#!/bin/bash

if [ ! -f install.sh ]; then
    echo "Must be in folder to install"
    exit 1
fi


if [ $(id -u) != 0 ]; then
    echo "Must be root"
    exit 1
fi

mkdir -p /usr/local/src/shijian
rm -rf /usr/local/src/shijian/*

rm /usr/local/bin/shijian
rm /usr/local/bin/sj

cp -r * /usr/local/src/shijian/
ln -s /usr/local/src/shijian/shijian.py /usr/local/bin/shijian
ln -s /usr/local/src/shijian/shijian.py /usr/local/bin/sj

echo "Done"