i=true

while [ $i ];
do
      ./run_sketch.sh &> out.txt
      fin="`cat out.txt | grep "Time limit exceeded"`"
      if [ -n "$fin" ]; then
	  cat out.txt | grep "Total time"
      	  printf "Failed!\n"
      else
      	  cat out.txt > out_short.txt
	  printf "DONE!\n"
	  break
      fi
done


