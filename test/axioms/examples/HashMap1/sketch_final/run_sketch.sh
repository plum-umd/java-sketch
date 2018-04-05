pwd=`pwd`
inline=3
unroll=5
debug=13
timeout=15
sketch --fe-tempdir ${pwd}/ --fe-keep-tmp --fe-output sk_HashTableTest --fe-inc ${pwd}/sk_HashTableTest ${pwd}/sk_HashTableTest/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline} --slv-timeout ${timeout} #--slv-simple-inputs --slv-randassign 
