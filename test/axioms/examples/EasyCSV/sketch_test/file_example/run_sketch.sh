pwd=`pwd`
inline=3
unroll=6
debug=13
timeout=10
sketch --fe-tempdir ${pwd} --fe-keep-tmp --fe-output sk_Tester --fe-inc ${pwd}/sk_Tester ${pwd}/sk_Tester/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline} --slv-timeout ${timeout} --slv-randassign --slv-simple-inputs #--bnd-arr-size 50
