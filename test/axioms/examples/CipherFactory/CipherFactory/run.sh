pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/tests/DefaultCipherFactoryTest.java ${pwd}/noax/tests/CipherFactoryTester.java ${pwd}/noax/ConfigurableCipherFactor.java ${pwd}/noax/DefaultCipherFactory.java ${pwd}/noax/CryptoManager.java ${pwd}/noax/ICipherFactory.java ${pwd}/noax/ICryptoManager.java model/ -o ${pwd}/../result_noax"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/ax/tests/DefaultCipherFactoryTest.java ${pwd}/ax/tests/CipherFactoryTester.java ${pwd}/ax/ConfigurableCipherFactor.java ${pwd}/ax/DefaultCipherFactory.java ${pwd}/ax/CryptoManager.java ${pwd}/ax/ICipherFactory.java ${pwd}/ax/ICryptoManager.java ${pwd}/../libs --no-lib -o ${pwd}/../result_ax"
elif [ "$1" == "3" ]
then
    shift
    # ./jsk.sh $@ "${pwd}/noax/Cryptographer_syn.java ${pwd}/noax/PasswordManager_syn.java ${pwd}/noax/PasswordMap.java ${pwd}/noax/PasswordManagerTest.java model/ -o ${pwd}/../result_noax"
    ./jsk.sh $@ "${pwd}/ax/tests/CipherFactoryTester.java ${pwd}/ax/ConfigurableCipherFactor.java ${pwd}/ax/DefaultCipherFactory.java ${pwd}/ax/CryptoManager_syn.java ${pwd}/ax/ICipherFactory.java ${pwd}/ax/ICryptoManager.java ${pwd}/../libs --no-lib -o ${pwd}/../result_ax"
fi



