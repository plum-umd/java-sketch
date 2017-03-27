#!/bin/bash

wd=`pwd`
APIS=(`ls input/api*`)
cd ../..
if [ $# -ge 1 ]
then
    in_num=$1
    shift

    python -m parser.parser -f $* tests/dataflow/input/api$in_num.java
else
    if [ ! -d tests/dataflow/tmp ]; then mkdir -p tests/dataflow/tmp
    else rm tests/dataflow/tmp/*
    fi

    # These are the 'regular' reaching def tests
    for (( i=0; i<${#APIS[@]}; i++ ))
    do
    	echo "python -m parser.parser -l40 -frv tests/dataflow/input/api$i.java > tests/dataflow/tmp/$i.out"
    	python -m parser.parser -l40 -frv tests/dataflow/input/api$i.java > tests/dataflow/tmp/$i.out
    done

    # inputs tests. need to be specific
    # api 0
    echo "python -m parser.parser -l40 -fvi -e0 -e0  tests/dataflow/input/api0.java > tests/dataflow/tmp/0_00.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e0 -e0  tests/dataflow/input/api0.java > tests/dataflow/tmp/0_00.out 2> $wd/log.out
    echo "python -m parser.parser -l40 -fvi -e0 -e1  tests/dataflow/input/api0.java > tests/dataflow/tmp/0_01.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e0 -e1  tests/dataflow/input/api0.java > tests/dataflow/tmp/0_01.out 2> $wd/log.out
    echo "python -m parser.parser -l40 -fvi -e1 -e1  tests/dataflow/input/api0.java > tests/dataflow/tmp/0_11.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e1 -e1  tests/dataflow/input/api0.java > tests/dataflow/tmp/0_11.out 2> $wd/log.out

    # api 1
    echo "python -m parser.parser -l40 -fvi -e 0 -e 0  tests/dataflow/input/api1.java > tests/dataflow/tmp/1_00.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 0 -e 0  tests/dataflow/input/api1.java > tests/dataflow/tmp/1_00.out 2> $wd/log.out
    
    # api 5
    echo "python -m parser.parser -l40 -fvi -e 0 -e 2  tests/dataflow/input/api5.java > tests/dataflow/tmp/5_02.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 0 -e 2  tests/dataflow/input/api5.java > tests/dataflow/tmp/5_02.out 2> $wd/log.out

    # api 6
    echo "python -m parser.parser -l40 -fvi -e 0 -e 3  tests/dataflow/input/api6.java > tests/dataflow/tmp/6_03.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 0 -e 3  tests/dataflow/input/api6.java > tests/dataflow/tmp/6_03.out 2> $wd/log.out

    # api 7
    echo "python -m parser.parser -l40 -fvi -e 1 -e 2  tests/dataflow/input/api7.java > tests/dataflow/tmp/7_12.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 1 -e 2  tests/dataflow/input/api7.java > tests/dataflow/tmp/7_12.out 2> $wd/log.out
    echo "python -m parser.parser -l40 -fvi -e 3 -e 4  tests/dataflow/input/api7.java > tests/dataflow/tmp/7_34.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 3 -e 4  tests/dataflow/input/api7.java > tests/dataflow/tmp/7_34.out 2> $wd/log.out

    # api 8
    echo "python -m parser.parser -l40 -fvi -e 1 -e 2  tests/dataflow/input/api8.java > tests/dataflow/tmp/8_12.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 1 -e 2  tests/dataflow/input/api8.java > tests/dataflow/tmp/8_12.out 2> $wd/log.out

    # api 9
    echo "python -m parser.parser -l40 -fvi -e 0 -e 0  tests/dataflow/input/api9.java > tests/dataflow/tmp/9_00.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 0 -e 0  tests/dataflow/input/api9.java > tests/dataflow/tmp/9_00.out 2> $wd/log.out
    echo "python -m parser.parser -l40 -fvi -e 0 -e 1  tests/dataflow/input/api9.java > tests/dataflow/tmp/9_01.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 0 -e 1  tests/dataflow/input/api9.java > tests/dataflow/tmp/9_01.out 2> $wd/log.out
    echo "python -m parser.parser -l40 -fvi -e 1 -e 1  tests/dataflow/input/api9.java > tests/dataflow/tmp/9_11.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 1 -e 1  tests/dataflow/input/api9.java > tests/dataflow/tmp/9_11.out 2> $wd/log.out
    echo "python -m parser.parser -l40 -fvi -e 0 -e 2  tests/dataflow/input/api9.java > tests/dataflow/tmp/9_02.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 0 -e 2  tests/dataflow/input/api9.java > tests/dataflow/tmp/9_02.out 2> $wd/log.out

    # api 10
    echo "python -m parser.parser -l40 -fvi -e 1 -e 2  tests/dataflow/input/api10.java > tests/dataflow/tmp/10_12.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 1 -e 2  tests/dataflow/input/api10.java > tests/dataflow/tmp/10_12.out 2> $wd/log.out
    echo "python -m parser.parser -l40 -fvi -e 1 -e 3  tests/dataflow/input/api10.java > tests/dataflow/tmp/10_13.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 1 -e 3  tests/dataflow/input/api10.java > tests/dataflow/tmp/10_13.out 2> $wd/log.out
    echo "python -m parser.parser -l40 -fvi -e 3 -e 3  tests/dataflow/input/api10.java > tests/dataflow/tmp/10_33.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 3 -e 3  tests/dataflow/input/api10.java > tests/dataflow/tmp/10_33.out 2> $wd/log.out

    # api 12
    echo "python -m parser.parser -l40 -fvi -e 1 -e 1  tests/dataflow/input/api12.java > tests/dataflow/tmp/12_11.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 1 -e 1  tests/dataflow/input/api12.java > tests/dataflow/tmp/12_11.out 2> $wd/log.out

    # api 14
    echo "python -m parser.parser -l40 -fvi -e 1 -e 3  tests/dataflow/input/api14.java > tests/dataflow/tmp/14_13.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 1 -e 3  tests/dataflow/input/api14.java > tests/dataflow/tmp/14_13.out 2> $wd/log.out

    # api 15
    echo "python -m parser.parser -l40 -fvi -e 1 -e 1  tests/dataflow/input/api15.java > tests/dataflow/tmp/15_11.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 1 -e 1  tests/dataflow/input/api15.java > tests/dataflow/tmp/15_11.out 2> $wd/log.out

    # api 16
    echo "python -m parser.parser -l40 -fvi -e 0 -e 0  tests/dataflow/input/api16.java > tests/dataflow/tmp/16_00.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 0 -e 0  tests/dataflow/input/api16.java > tests/dataflow/tmp/16_00.out 2> $wd/log.out

    # api 17
    echo "python -m parser.parser -l40 -fvi -e 0 -e 1  tests/dataflow/input/api17.java > tests/dataflow/tmp/17_01.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 0 -e 1  tests/dataflow/input/api17.java > tests/dataflow/tmp/17_01.out 2> $wd/log.out

    # api 19
    echo "python -m parser.parser -l40 -fvi -e 2 -e 2  tests/dataflow/input/api19.java > tests/dataflow/tmp/19_22.out 2> $wd/log.out"
    python -m parser.parser -l40 -fvi -e 2 -e 2  tests/dataflow/input/api19.java > tests/dataflow/tmp/19_22.out 2> $wd/log.out

    cd tests/dataflow
    diff -r -x ".gitignore" -x ".DS_Store" out tmp > results.out

    if [ -s results.out ]
    then echo "Tests failed.";
    else echo "Tests passed!";
    fi
fi
