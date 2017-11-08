#!/bin/bash
loops="35"
inline="5"
debug="-V 13"
args="--fe-tempdir /Users/grumpy/Research/java-sketch/test/axioms/examples/HashMap1/HashMap/../sketch --fe-keep-tmp --fe-output sk_HashTableTest --fe-inc /Users/grumpy/Research/java-sketch/test/axioms/examples/HashMap1/HashMap/../sketch/sk_HashTableTest /Users/grumpy/Research/java-sketch/test/axioms/examples/HashMap1/HashMap/../sketch/sk_HashTableTest/main.sk --bnd-unroll-amnt $loops --bnd-inline-amnt $inline $debug"

sketch $args

