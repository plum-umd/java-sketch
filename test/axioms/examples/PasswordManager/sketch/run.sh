#!/bin/bash
loops="16"
inline="2"
debug="-V 13"
# args="--fe-tempdir /Users/kathymariano/Research/java-sketch/test/axioms/examples/PasswordManager/PasswordManager/../sketch --fe-keep-tmp --fe-output sk_PasswordManagerTest --fe-inc /Users/kathymariano/Research/java-sketch/test/axioms/examples/PasswordManager/PasswordManager/../sketch/sk_PasswordManagerTest /Users/kathymariano/Research/java-sketch/test/axioms/examples/PasswordManager/PasswordManager/../sketch/sk_PasswordManagerTest/main.sk --bnd-unroll-amnt $loops --bnd-inline-amnt $inline $debug"
args="--fe-tempdir /Users/kathymariano/Research/java-sketch2/test/axioms/examples/PasswordManager/PasswordManager/../sketch --fe-keep-tmp --fe-output sk_PasswordManagerTest --fe-inc /Users/kathymariano/Research/java-sketch2/test/axioms/examples/PasswordManager/PasswordManager/../sketch/sk_PasswordManagerTest /Users/kathymariano/Research/java-sketch2/test/axioms/examples/PasswordManager/PasswordManager/../sketch/sk_PasswordManagerTest/main.sk --V 13 --bnd-inline-amnt $inline --bnd-unroll-amnt $loops"

sketch $args

