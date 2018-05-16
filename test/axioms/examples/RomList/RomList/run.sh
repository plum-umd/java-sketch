pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/ax/Tester.java ${pwd}/ax/RomlistGame.java ${pwd}/ax/RomlistParser.java ${pwd}/../libs --no-lib -o ${pwd}/../result_ax"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/ax/Tester.java ${pwd}/ax/RomlistGame.java ${pwd}/ax/RomlistParser_syn.java ${pwd}/../libs --no-lib -o ${pwd}/../result_ax"
elif [ "$1" == "3" ]
then
    shift
    ./jsk.sh $@ "${pwd}/ax/Cryptographer_syn.java ${pwd}/ax/PasswordManager_syn.java ${pwd}/ax/PasswordMap.java ${pwd}/ax/PasswordManagerTest.java model/ -o ${pwd}/../result_ax"
fi



