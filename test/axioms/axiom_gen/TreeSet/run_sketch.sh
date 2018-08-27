sketch $1/main.sk --fe-tempdir result --fe-keep-tmp --fe-output sk_TreeSetTester --fe-inc $1 --bnd-inline-amnt 15 --V 13 --bnd-int-range 32

cd $1
rm *~
cd ..
rm *~
