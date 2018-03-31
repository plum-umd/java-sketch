pwd=`pwd`
inline=2
unroll=16
debug=13
timeout=15
sketch --fe-tempdir ${pwd}/ --fe-keep-tmp --fe-output sk_PasswordManagerTest --fe-inc ${pwd}/sk_PasswordManagerTest ${pwd}/sk_PasswordManagerTest/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline} --slv-timeout ${timeout} #--slv-simple-inputs --slv-randassign 
