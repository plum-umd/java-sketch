pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/*.java model/org/junit/Assert.java model/lang/Integer.java model/lang/Number.java model/util/ArrayList.java -o ${pwd}/../result_noax/"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/Bucketing_loops.java ${pwd}/BucketingTest.java ${pwd}/Pair.java ${pwd}/HashTable.java ${pwd}/../libs/ --no-lib -o ${pwd}/../result_ax/"
    # ./jsk.sh $@ "${pwd}/Bucketing_loops.java ${pwd}/BucketingTest.java ${pwd}/Pair.java ${pwd}/HashTable.java ${pwd}/../libs/ --no-lib -o ${pwd}/../result_ax/"
fi
