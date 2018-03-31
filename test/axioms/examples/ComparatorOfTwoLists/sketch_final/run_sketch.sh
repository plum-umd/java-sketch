pwd=`pwd`
inline=2
unroll=10
debug=13
timeout=10
sketch --fe-tempdir ${pwd}/ --fe-keep-tmp --fe-output sk_Comparator --fe-inc ${pwd}/sk_Comparator ${pwd}/sk_Comparator/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline} --slv-timeout ${timeout} --slv-randassign #--slv-simple-inputs  #--bnd-arr-size 50
