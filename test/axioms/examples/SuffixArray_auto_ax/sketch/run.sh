#!/bin/bash
loops="15"
inline="2"
debug="-V 13"
args="--fe-tempdir /Users/grumpy/Research/java-sketch2/test/axioms/examples/SuffixArray_auto_ax/SuffixArray/../sketch/ --fe-keep-tmp --fe-output sk_SuffixArrayTest --fe-inc /Users/grumpy/Research/java-sketch2/test/axioms/examples/SuffixArray_auto_ax/SuffixArray/../sketch/sk_SuffixArrayTest /Users/grumpy/Research/java-sketch2/test/axioms/examples/SuffixArray_auto_ax/SuffixArray/../sketch/sk_SuffixArrayTest/main.sk --bnd-unroll-amnt $loops --bnd-inline-amnt $inline $debug"

sketch $args
