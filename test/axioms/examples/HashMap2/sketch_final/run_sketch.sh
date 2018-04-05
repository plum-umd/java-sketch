pwd=`pwd`
inline=1
unroll=2
debug=13
timeout=10
sketch --fe-tempdir ${pwd} --fe-keep-tmp --fe-output sk_BucketingTest --fe-inc ${pwd}/sk_BucketingTest ${pwd}/sk_BucketingTest/main.sk --V ${debug} --bnd-unroll-amnt ${unroll} --bnd-inline-amnt ${inline}  --slv-timeout ${timeout} #--slv-simple-inputs --slv-randassign #--bnd-arr-size 50
