#!/bin/bash
loops="10"
inline="3"
debug="-V 13"
args="--fe-tempdir /Users/grumpy/Research/java-sketch/test/axioms/examples/PasswordManager/PasswordManager/../sketch --fe-keep-tmp --fe-output sk_PasswordManagerTest --fe-inc /Users/grumpy/Research/java-sketch/test/axioms/examples/PasswordManager/PasswordManager/../sketch/sk_PasswordManagerTest /Users/grumpy/Research/java-sketch/test/axioms/examples/PasswordManager/PasswordManager/../sketch/sk_PasswordManagerTest/main.sk --bnd-unroll-amnt $loops --bnd-inline-amnt $inline $debug"

sketch $args

