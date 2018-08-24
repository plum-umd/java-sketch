TEST=test/axioms/axiom_gen/ArrayList
cd ../../../../

./jsk.sh ${TEST}/ArrayListTester$1.java ${TEST}/Object.java ${TEST}/Integer.java ${TEST}/ArrayList$1.java --no-lib

cd ${TEST}
rm *~
