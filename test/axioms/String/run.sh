#!/bin/bash
echo > ad_t8_noassert.txt
# echo > i_t8_noassert.txt
for (( i=1; i<=30; i++ ))
do
    echo "python run.py --ad -n15 -f8 -l8 -I$i >> ad_t8.txt"
    python run.py --ad -n15 -f8 -l8 -I$i >> ad_t8.txt
done
# for (( i=1; i<=30; i++ ))
# do
#     echo "python run.py -i -n15 -f8 -l8 -I$i >> i_t8_noassert.txt"
#     python run.py -i -n15 -f8 -l8 -I$i >> i_t8_noassert.txt
# done
