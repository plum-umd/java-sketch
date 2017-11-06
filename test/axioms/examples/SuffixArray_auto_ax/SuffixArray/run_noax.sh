pwd=`pwd`
cd ../../../../../
# ./jsk.sh $@ "${pwd}/tests/SuffixArrayTest.java ${pwd}/SuffixArray.java ${pwd}/Arrays.java ${pwd}/SuffixRankTuple.java ${pwd}/TwoDArray.java model/org/junit/Assert.java model/lang/Integer.java model/lang/Number.java model/util/HashMap.java model/lang/String.java model/lang/CharSequence.java model/lang/Comparable.java model/util/TreeSet.java model/util/Deque.java model/util/ArrayDeque.java model/util/HashSet.java model/util/HashMap_Simple.java model/util/Map.java model/org/junit/Assert.java model/util/Set.java"
# ./jsk.sh $@ "${pwd}/SuffixArray.java model/"

# ./jsk.sh $@ "${pwd}/SuffixArray.java model/ ${pwd}/tests/SuffixArrayTest.java ${pwd}/SuffixRankTuple.java ${pwd}/../libs"

./jsk.sh $@ "${pwd}/tests/SuffixArrayTest.java ${pwd}/SuffixArray.java ${pwd}/../libs/jsketch/ model/ -o ${pwd}/../result_noax/ --no-lib"

