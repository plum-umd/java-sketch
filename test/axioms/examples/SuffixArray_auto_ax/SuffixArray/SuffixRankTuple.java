// Helper class which sorts suffix ranks
// CHANGE
public class SuffixRankTuple {
// public class SuffixRankTuple implements Comparable <SuffixRankTuple> {          
// static class SuffixRankTuple implements Comparable <SuffixRankTuple> {      
    
    int firstHalf, secondHalf, originalIndex;
    
    // // Sort Suffix ranks first on the first half then the second half
    // public int compareTo(SuffixRankTuple other) {
    // 	int cmp = Integer.compare(firstHalf, other.firstHalf);
    // 	if (cmp == 0) cmp = Integer.compare(secondHalf, other.secondHalf);
    // 	// CHANGE
    // 	if (cmp == 0) return Integer.compare(originalIndex, other.originalIndex);
    // 	return cmp;
    // }
    
    // public String toString() {
    // 	// String s1 = String.concat(originalIndex.toString(), " -> (");
    // 	// String s2 = String.concat(firstHalf.toString(), ", ");
    // 	// String s3 = String.concat(secondHalf.toString(), ")");
    // 	// String s4 = String.concat(s1, s2);
    // 	// String s5 = String.concat(s4, s3);
    // 	// return s5;
    // 	// return originalIndex + " -> (" + firstHalf + ", " + secondHalf + ")";
    // 	return "Blah!";	  
    // }
    
}
