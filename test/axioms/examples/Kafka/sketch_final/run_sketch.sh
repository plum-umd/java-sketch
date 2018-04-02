pwd=`pwd`
inline=1
unroll=15 #35
debug=13
timeout=15
sketch --fe-tempdir ${pwd}/ --fe-keep-tmp --fe-output sk_Tester --fe-inc ${pwd}/sk_Tester ${pwd}/sk_Tester/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline} --slv-timeout ${timeout} #--slv-simple-inputs --slv-randassign 
