pwd=`pwd`
inline=2
unroll=35
debug=13
timeout=15
sketch --fe-tempdir ${pwd}/../result_noax/ --fe-keep-tmp --fe-output sk_Tester --fe-inc ${pwd}/../result_noax/sk_Tester ${pwd}/../result_noax/sk_Tester/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline}  --slv-timeout ${timeout} #--bnd-arr-size 50
