sketch $1/main.sk --bnd-inline-amnt 5 --bnd-unroll-amnt 3 --bnd-arr-size 32 --fe-tempdir result --fe-keep-tmp --fe-output sk_HashTableTest --fe-inc $1 --bnd-int-range 32 #--slv-timeout 10 

cd $1
rm *~
cd ..
rm *~
