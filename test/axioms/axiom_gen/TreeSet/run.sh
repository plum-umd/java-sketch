TEST=test/axioms/axiom_gen/TreeSet
cd ../../../../

./jsk.sh ${TEST}/TreeSetTester$1.java ${TEST}/Object.java ${TEST}/Integer.java ${TEST}/TreeSet$1.java --no-lib

cd ${TEST}
rm *~
