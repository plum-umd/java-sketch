#!/bin/bash
echo "python run_impl.py"
python run_impl.py $1
echo "python run_adt.py"
python run_adt.py $1
echo "python combine.py"
python combine.py
