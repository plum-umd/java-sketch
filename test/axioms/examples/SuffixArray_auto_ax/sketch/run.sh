#!/bin/bash
loops="40"
inline="10"
debug="-V 13"
args="--fe-tempdir /Users/grumpy/Research/java-sketch/test/axioms/examples/SuffixArray_auto_ax/SuffixArray/../sketch/ --fe-keep-tmp --fe-output sk_SuffixArrayTest --fe-inc /Users/grumpy/Research/java-sketch/test/axioms/examples/SuffixArray_auto_ax/SuffixArray/../sketch/sk_SuffixArrayTest /Users/grumpy/Research/java-sketch/test/axioms/examples/SuffixArray_auto_ax/SuffixArray/../sketch/sk_SuffixArrayTest/main.sk --bnd-unroll-amnt $loops --bnd-inline-amnt $inline $debug"

sketch $args
