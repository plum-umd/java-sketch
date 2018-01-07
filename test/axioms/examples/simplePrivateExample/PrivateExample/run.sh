pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/PrivateExample.java model/org/junit/Assert.java model/lang/Integer.java model/lang/Number.java model/crypto/ -o ${pwd}/../result_noax/"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/PrivateExample_ax.java ${pwd}/../libs/ --no-lib -o ${pwd}/../result_ax/"
elif [ "$1" == "3" ]
then
    shift
    ./jsk.sh $@ "${pwd}/PrivateExample_ax.java ${pwd}/../libs/ --no-lib -o ${pwd}/../result_ax/" | grep "TYPE"
fi
