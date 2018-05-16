pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/PQueue.java model/ -o ${pwd}/../result_noax"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/ax/PQueue.java ${pwd}/../libs/model/lang/Integer.java ${pwd}/../libs/model/lang/Number.java ${pwd}/../libs/model/lang/Object.java ${pwd}/../libs/axioms/util/ -o ${pwd}/../result_ax --no-lib"
fi
