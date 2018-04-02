pwd=`pwd`
inline=2
unroll=9 #25
debug=13
timeout=15
sketch --fe-tempdir ${pwd}/ --fe-keep-tmp --fe-output sk_CipherFactoryTests --fe-inc ${pwd}/sk_CipherFactoryTests ${pwd}/sk_CipherFactoryTests/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline} --slv-timeout ${timeout} #--slv-simple-inputs --slv-randassign 
