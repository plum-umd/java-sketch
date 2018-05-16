pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Tester.java ${pwd}/noax/CommunicationWithFiles.java ${pwd}/noax/Comparator.java model/ -o ${pwd}/../result_noax"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Tester.java ${pwd}/noax/CommunicationWithFiles.java ${pwd}/noax/Comparator.java ${pwd}/../libs/ -o ${pwd}/../result_ax --no-lib"
    # ./jsk.sh $@ "${pwd}/ax/Tester.java ${pwd}/ax/CommunicationWithFiles_syn.java ${pwd}/ax/Comparator.java ${pwd}/../libs/ -o ${pwd}/../result_ax --no-lib"
elif [ "$1" == "3" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Cryptographer_syn.java ${pwd}/noax/PasswordManager_syn.java ${pwd}/noax/PasswordMap.java ${pwd}/noax/PasswordManagerTest.java model/ -o ${pwd}/../result_noax"
fi



