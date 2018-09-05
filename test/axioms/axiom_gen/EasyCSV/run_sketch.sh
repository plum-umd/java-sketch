sketch $1/main.sk --bnd-inline-amnt 5 --bnd-unroll-amnt 5 --bnd-arr-size 32 --slv-timeout 10 --fe-tempdir result --fe-keep-tmp --fe-output sk_CSVTester --fe-inc $1 #--bnd-int-range 32

cd $1
rm *~
cd ..
rm *~
