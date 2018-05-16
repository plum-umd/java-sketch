pwd=`pwd`
inline=2 #3
unroll=8
debug=13
timeout=10
sketch --fe-tempdir ${pwd}/ --fe-keep-tmp --fe-output sk_SuffixArrayTest --fe-inc ${pwd}/sk_SuffixArrayTest ${pwd}/sk_SuffixArrayTest/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline} --slv-timeout ${timeout} #--slv-simple-inputs #--slv-randassign #--bnd-arr-size 50
