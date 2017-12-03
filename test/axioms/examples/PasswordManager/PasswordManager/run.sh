pwd=`pwd`
cd ../../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/Cryptographer.java ${pwd}/PasswordManager.java ${pwd}/PasswordMap.java ${pwd}/PasswordManagerTest.java model/ -o ${pwd}/../result_noax"
fi



