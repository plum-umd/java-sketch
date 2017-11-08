#!/bin/bash

pwd=`pwd`
cd ../../../../../
if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/HashTable.java ${pwd}/HashTableTest.java ${pwd}/HashTableNode.java model/org/junit/Assert.java model/lang/Integer.java model/lang/Number.java model/util/ArrayList.java -o ${pwd}/../result_noax"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/HashTable_loops.java ${pwd}/HashTableTest.java ${pwd}/HashTableNode.java model/org/junit/Assert.java model/lang/Integer.java model/lang/Number.java model/util/ArrayList.java -o ${pwd}/../result_noax"
elif [ "$1" == "3" ]
then
    shift
    ./jsk.sh $@ "${pwd}/HashTable_equals.java ${pwd}/HashTableTest.java ${pwd}/HashTableNode.java model/org/junit/Assert.java model/lang/Integer.java model/lang/Number.java model/util/ArrayList.java -o ${pwd}/../result_noax"

elif [ "$1" == "4" ]
then
    shift
    ./jsk.sh $@ "${pwd}/HashTable.java ${pwd}/HashTableTest.java ${pwd}/HashTableNode.java ${pwd}/../libs/ -o ${pwd}/../result_ax --no-lib"
elif [ "$1" == "5" ]
then
    shift
    ./jsk.sh $@ "${pwd}/HashTable_loops.java ${pwd}/HashTableTest.java ${pwd}/HashTableNode.java ${pwd}/../libs/ -o ${pwd}/../result_ax --no-lib"
elif [ "$1" == "6" ]
then
    shift
    ./jsk.sh $@ "${pwd}/HashTable_equals.java ${pwd}/HashTableTest.java ${pwd}/HashTableNode.java ${pwd}/../libs/ -o ${pwd}/../result_ax --no-lib"
fi
