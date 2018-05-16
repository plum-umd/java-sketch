#!/bin/bash
loops="35"
inline="5"
debug="-V 13"
args="--fe-tempdir /Users/kathymariano/Research/java-sketch2/test/axioms/examples/HashMap2/HashMap/../sketch/ --fe-keep-tmp --fe-output sk_BucketingTest --fe-inc /Users/kathymariano/Research/java-sketch2/test/axioms/examples/HashMap2/HashMap/../sketch/sk_BucketingTest /Users/kathymariano/Research/java-sketch2/test/axioms/examples/HashMap2/HashMap/../sketch/sk_BucketingTest/main.sk --bnd-unroll-amnt $loops --bnd-inline-amnt $inline $debug"

sketch $args

