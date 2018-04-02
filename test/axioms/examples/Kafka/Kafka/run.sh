pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Tester.java ${pwd}/noax/ICipher.java ${pwd}/noax/JCECipher.java ${pwd}/noax/CipherFactory.java ${pwd}/noax/OpenSSLCipher.java model/ -o ${pwd}/../result_noax"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Tester.java ${pwd}/noax/ICipher.java ${pwd}/noax/JCECipher_syn.java ${pwd}/noax/CipherFactory.java ${pwd}/noax/OpenSSLCipher_syn.java model/ -o ${pwd}/../result_noax"
elif [ "$1" == "3" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Cryptographer_syn.java ${pwd}/noax/PasswordManager_syn.java ${pwd}/noax/PasswordMap.java ${pwd}/noax/PasswordManagerTest.java model/ -o ${pwd}/../result_noax"
fi



