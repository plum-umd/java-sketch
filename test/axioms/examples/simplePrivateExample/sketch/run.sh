#!/bin/bash
loops="35"
inline="5"
debug="-V 13"
args="--fe-tempdir /Users/grumpy/Research/java-sketch/test/axioms/examples/simplePrivateExample/PrivateExample/../sketch/ --fe-keep-tmp --fe-output sk_PrivateExample --fe-inc /Users/grumpy/Research/java-sketch/test/axioms/examples/simplePrivateExample/PrivateExample/../sketch/sk_PrivateExample /Users/grumpy/Research/java-sketch/test/axioms/examples/simplePrivateExample/PrivateExample/../sketch/sk_PrivateExample/main.sk --bnd-unroll-amnt $loops --bnd-inline-amnt $inline $debug"

sketch $args

