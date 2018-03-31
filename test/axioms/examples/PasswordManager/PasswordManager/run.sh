pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Cryptographer_syn.java ${pwd}/noax/PasswordManager.java ${pwd}/noax/PasswordMap.java ${pwd}/noax/PasswordManagerTest.java model/ -o ${pwd}/../result_noax"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Cryptographer_syn.java ${pwd}/noax/PasswordManager_syn.java ${pwd}/noax/PasswordMap.java ${pwd}/noax/PasswordManagerTest.java model/io model/lang/ model/org model/security model/util model/crypto/KerberosKey.java model/crypto/Key.java model/crypto/KeyGenerator.java model/crypto/Mac.java model/crypto/SecretKey.java model/crypto/spec ../model2/crypto/Cipher.java -o ${pwd}/../result_noax"
    # ./jsk.sh $@ "${pwd}/ax/PasswordManagerTest.java ${pwd}/ax/PasswordManager.java ${pwd}/ax/PasswordMap.java ${pwd}/ax/Cryptographer.java ${pwd}/../libs/ -o ${pwd}/../result_ax --no-lib"
elif [ "$1" == "3" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Cryptographer_syn.java ${pwd}/noax/PasswordManager_syn.java ${pwd}/noax/PasswordMap.java ${pwd}/noax/PasswordManagerTest.java model/ -o ${pwd}/../result_noax"
fi



