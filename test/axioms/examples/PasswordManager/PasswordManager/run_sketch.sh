pwd=`pwd`
inline=2
unroll=16
debug=13
timeout=15
sketch --fe-tempdir ${pwd}/../result_noax/ --fe-keep-tmp --fe-output sk_PasswordManagerTest --fe-inc ${pwd}/../result_noax/sk_PasswordManagerTest ${pwd}/../result_noax/sk_PasswordManagerTest/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline}  --slv-timeout ${timeout} #--bnd-arr-size 50
