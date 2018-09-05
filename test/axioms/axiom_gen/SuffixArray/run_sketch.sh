sketch $1/main.sk --bnd-inline-amnt 3 --bnd-unroll-amnt 8 --bnd-arr-size 32 --slv-timeout 10 --fe-tempdir result --fe-keep-tmp --fe-output sk_SuffixArrayTest --fe-inc $1

# sketch $1/main.sk --fe-tempdir result --fe-keep-tmp --fe-output sk_TreeSetTester --fe-inc $1 --bnd-inline-amnt 15 --V 13 --bnd-int-range 32

cd $1
rm *~
cd ..
rm *~
