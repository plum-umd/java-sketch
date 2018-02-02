pwd=`pwd`
cd ../../../../../

if [ "$1" == "1" ]
then
    shift
    ./jsk.sh $@ "${pwd}/ax/tests/Tester.java ${pwd}/ax/CsvDocument.java ${pwd}/ax/tests/CsvDocumentTest.java ${pwd}/ax/tests/CsvRowTest.java ${pwd}/ax/tests/CsvColumnTest.java ${pwd}/ax/CodeAssertion.java ${pwd}/ax/CsvColumn.java ${pwd}/ax/CsvRow.java ${pwd}/ax/CsvConfiguration.java model/ -o ${pwd}/../result_noax"
    # ./jsk.sh $@ "${pwd}/noax/tests/Tester.java ${pwd}/noax/CsvDocument.java ${pwd}/noax/tests/CsvDocumentTest.java ${pwd}/noax/tests/CsvRowTest.java ${pwd}/noax/tests/CsvColumnTest.java ${pwd}/noax/CodeAssertion.java ${pwd}/noax/CsvColumn.java ${pwd}/noax/CsvRow.java ${pwd}/noax/CsvConfiguration.java model/ -o ${pwd}/../result_noax"
elif [ "$1" == "2" ]
then
    shift
    ./jsk.sh $@ "${pwd}/ax/tests/Tester.java ${pwd}/ax/CsvDocument_syn.java ${pwd}/ax/tests/CsvDocumentTest.java ${pwd}/ax/tests/CsvRowTest.java ${pwd}/ax/tests/CsvColumnTest.java ${pwd}/ax/CodeAssertion.java ${pwd}/ax/CsvColumn.java ${pwd}/ax/CsvRow.java ${pwd}/ax/CsvConfiguration.java model/ -o ${pwd}/../result_noax"
    # ./jsk.sh $@ "${pwd}/ax/tests/Tester.java ${pwd}/ax/CsvDocument.java ${pwd}/ax/tests/CsvDocumentTest.java ${pwd}/ax/tests/CsvRowTest.java ${pwd}/ax/tests/CsvColumnTest.java ${pwd}/ax/CodeAssertion.java ${pwd}/ax/CsvColumn.java ${pwd}/ax/CsvRow.java ${pwd}/ax/CsvConfiguration.java --no-lib ${pwd}/../libs/ -o ${pwd}/../result_ax"
elif [ "$1" == "3" ]
then
    shift
    ./jsk.sh $@ "${pwd}/noax/Cryptographer_syn.java ${pwd}/noax/PasswordManager_syn.java ${pwd}/noax/PasswordMap.java ${pwd}/noax/PasswordManagerTest.java model/ -o ${pwd}/../result_noax"
fi



