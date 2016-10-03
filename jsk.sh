#!/bin/bash

if [[ $1 == "-test" ]]
then
    wd=`pwd`
    if [ ! -d $wd/tmp ]; then mkdir -p $wd/tmp
    else rm $wd/tmp/*
    fi

    shift
    in=$1
    shift
    python -m java_sk.main -o result/tmp $wd/$in
    
    diff -Bwr result/tmp results/output
else
    python -m java_sk.main $@
fi
