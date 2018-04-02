pwd=`pwd`
inline=2
unroll=15
debug=13
timeout=15
sketch --fe-tempdir ${pwd}/../result_noax/ --fe-keep-tmp --fe-output sk_CipherFactoryTests --fe-inc ${pwd}/../result_noax/sk_CipherFactoryTests ${pwd}/../result_noax/sk_CipherFactoryTests/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline}  --slv-timeout ${timeout} #--bnd-arr-size 50
