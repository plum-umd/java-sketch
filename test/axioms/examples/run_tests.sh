printf "AXIOM RESULTS\n" > results.csv
## declare an array variable
# declare -a arr=(
# 	        "EasyCSV"
# 	       )
declare -a arr=(
    "SuffixArray_auto_ax"
    "HashMap1"
    "HashMap2"
    "PasswordManager"
    "CipherFactory"
    "Kafka"
    "EasyCSV"
    "RomList"
    "ComparatorOfTwoLists"
)

## now loop through the above array
for i in "${arr[@]}"
do
    printf "\n$i\n" >> results.csv
    printf "Running $i...\n"
    cd "$i/sketch_final/"
    # errormsg=`(gtimeout 10 ./run.sh 2 | grep "Exception") 2>&1`
    # printf "$errormsg"
    # if [ -n "$errormsg" ]; then
    # 	printf " ERROR\n" >> ../../results.csv
    # else
    for j in {1..31}
    do
	printf "$j\n"
	# ./run_sketch.sh | grep "Total time" | cut -d "=" -f 2 >> results.csv
	(./run_sketch.sh | grep "Total time" | cut -d "=" -f 2) >> ../../results.csv 2>> ../../error.txt
    done
    # fi
    printf "Finished $i.\n\n"    
    cd ../..
done

