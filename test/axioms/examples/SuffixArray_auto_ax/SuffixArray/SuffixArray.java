/**
 *
 * Generally speaking, suffix arrays are used to do multiple queries 
 * efficiently on one piece of data rather than to do one operation 
 * then move on to another piece of text.
 *
 * Good suffix array read: http://www.cs.yale.edu/homes/aspnes/pinewiki/SuffixArrays.html
 *
 * @author William Fiset, william.alexandre.fiset@gmail.com
 **/

import java.util.*;

class SuffixArray {

  // Size of the suffix array
  int N; 

  // T is the text
  int[] T;

  // Suffix array. Contains the indexes of sorted suffixes.
  int[] sa;

  // Contains Longest Common Prefix (LCP) count between adjacent suffixes.
  // lcp[i] = longestCommonPrefixLength( suffixes[i], suffixes[i+1] ).
  // Also, LCP[len-1] = 0
  int [] lcp;

    // CHANGE
    public int[] clone(int[] arr) {
  	int l = arr.length;
  	int[] arr_cp = new int[l];
  	for(int i=0; i<l; i++) {
  	    arr_cp[i] = arr[i];
  	}
  	return arr_cp;
    }

  public SuffixArray(String text) {
    this(toIntArray(text));
  }

    //CHANGE
    private static String intArrToString(int [] text) {
  	char[] tmp = new char[text.length];      
  	for (int i=0; i<text.length; i++) {
  	    tmp[i] = (char) text[i];
  	}
	
  	// Extract part of the suffix we need to compare
        return new String(tmp, 0, text.length);
    }
    
  private static int[] toIntArray(String s) {
    int[] text = new int[s.length()];
    for(int i=0;i<s.length();i++)text[i] = s.charAt(i);
    return text;
  }

  public SuffixArray(int[] text) {
      // CHANGE
    // if (text == null) throw new IllegalArgumentException();
    // T = text.clone();
    T = clone(text);
    N = text.length;    
    construct();
    kasai();
  }

  // Construct a suffix array in O(nlog^2(n))
  public void construct() {

    sa = new int[N];

    // Maintain suffix ranks in both a matrix with two rows containing the
    // current and last rank information as well as some sortable rank objects
    // CHANGE
    // int[][] suffixRanks = new int[2][N];
    TwoDArray suffixRanks = new TwoDArray(2, N);
    SuffixRankTuple[] ranks = new SuffixRankTuple[N];

    // Assign a numerical value to each character in the text
    for (int i = 0; i < N; i++) {
  	// CHANGE
  	// suffixRanks[0][i] = T[i];
  	suffixRanks.set(0, i, T[i]);
  	ranks[i] = new SuffixRankTuple();
    }

    // O(logn)
    for(int pos = 1; pos < N; pos *= 2) {

      for(int i = 0; i < N; i++) {
        SuffixRankTuple suffixRank = ranks[i];
        suffixRank.firstHalf  = suffixRanks.get(0, i);
  	// CHANGE
        // suffixRank.firstHalf  = suffixRanks[0][i];
        suffixRank.secondHalf = i+pos < N ? suffixRanks.get(0, i+pos) : -1;
  	// CHANGE
        // suffixRank.secondHalf = i+pos < N ? suffixRanks[0][i+pos] : -1;	
        suffixRank.originalIndex = i;
      }

      // O(nlogn)
      // CHANGE
      // java.util.Arrays.sort(ranks);
      ranks = Arrays.sort(ranks, ranks.length);


      int newRank = 0;
      suffixRanks.set(1, ranks[0].originalIndex, 0);
      // CHANGE
      // suffixRanks[1][ranks[0].originalIndex] = 0;

      for (int i = 1; i < N; i++ ) {
        
        SuffixRankTuple lastSuffixRank = ranks[i-1];
        SuffixRankTuple currSuffixRank = ranks[i];
  
        // If the first half differs from the second half
        if (currSuffixRank.firstHalf  != lastSuffixRank.firstHalf ||
            currSuffixRank.secondHalf != lastSuffixRank.secondHalf)
          newRank++;

        suffixRanks.set(1, currSuffixRank.originalIndex, newRank);

  	// CHANGE
        // suffixRanks[1][currSuffixRank.originalIndex] = newRank;

      }
      
      // Place top row (current row) to be the last row
      suffixRanks.setRow(0, suffixRanks.getRow(1));

      // CHANGE
      // suffixRanks[0] = suffixRanks[1];      
      // Optimization to stop early 
      // CHANGE
      // if (newRank == N-1) break;
      if (newRank == N-1) pos = N;      

    }

    // Fill suffix array
    for (int i = 0; i < N; i++) {
      sa[i] = ranks[i].originalIndex;
      ranks[i] = null;
    }

    // Cleanup
    suffixRanks = null;
    // CHANGE
    // suffixRanks[0] = suffixRanks[1] = null;
    suffixRanks = null;
    ranks = null;

  }

  // Constructs the LCP (longest common prefix) array in linear time - O(n)
  // http://www.mi.fu-berlin.de/wiki/pub/ABI/RnaSeqP4/suffix-array.pdf
  private void kasai() {

    lcp = new int[N];
    
    // Compute inverse index values
    int [] inv = new int[N];
    for (int i = 0; i < N; i++)
      inv[sa[i]] = i;

    // Current lcp length
    int len = 0;

    for (int i = 0; i < N; i++) {
      if (inv[i] > 0) {

        // Get the index of where the suffix below is
        int k = sa[inv[i]-1];
        // Compute lcp length. For most loops this is O(1)
        while( (i + len < N) && (k + len < N) && T[i+len] == T[k+len] )
          len++;

        lcp[inv[i]-1] = len;
        if (len > 0) len--;

      }
    }

  }

  // // Runs on O(mlog(n)) where m is the length of the substring
  // // and n is the length of the text.
  // // NOTE: This is the naive implementation. There exists an
  // // implementation which runs in O(m + log(n)) time
  // public boolean contains(String substr) {

  //   if (substr == null) return false;
  //   if (substr.equals("")) return true;

  //   String suffix_str;
  //   int lo = 0, hi = N - 1;
  //   int substr_len = substr.length();

  //   while( lo <= hi ) {
	
  //     int mid = (lo + hi) / 2;
  //     int suffix_index = sa[mid];
  //     int suffix_len = N - suffix_index;
      
  //     // CHANGE
  //     char[] tmp = new char[T.length];      
  //     for (int i=0; i<T.length; i++) {
  // 	  tmp[i] = (char) T[i];
  //     }

  //     // Extract part of the suffix we need to compare
  //     if (suffix_len <= substr_len) suffix_str = new String(tmp, suffix_index, suffix_len);
  //     else suffix_str = new String(tmp, suffix_index, substr_len);
  //     // CHANGE
  //     // if (suffix_len <= substr_len) suffix_str = new String(T, suffix_index, suffix_len);
  //     // else suffix_str = new String(T, suffix_index, substr_len);
      
  //     int cmp = suffix_str.compareTo(substr);

  //     // Found a match
  //     if ( cmp == 0 ) {
  //       // To find the first occurrence linear scan up/down
  //       // from here or keep doing binary search
  //       return true;
      
  //     // Substring is found above
  //     } else if (cmp < 0) {
  //       lo = mid + 1;

  //     // Substring is found below
  //     } else {
  //       hi = mid - 1;
  //     }

  //   }

  //   return false;

  // }

  // Finds the LRS(s) (Longest Repeated Substring) that occurs in a string.
  // Traditionally we are only interested in substrings that appear at
  // least twice, so this method returns an empty set if this is the case.
  // @return an ordered set of longest repeated substrings
  public TreeSet <String> lrs() {

    int max_len = 0;
    TreeSet <String> lrss = new TreeSet<>();

    // CHANGE
    char[] tmp = new char[T.length];      
    for (int i=0; i<T.length; i++) {
    	tmp[i] = (char) T[i];
    }
    
    for (int i = 0; i < N; i++) {
      if (lcp[i] > 0 && lcp[i] >= max_len) {
        
        // We found a longer LRS
        if ( lcp[i] > max_len )
          lrss.clear();
        
        // Append substring to the list and update max
        max_len = lcp[i];
    	// CHANGE
        lrss.add( new String(tmp, sa[i], max_len) );
    	// lrss.add( new String(T, sa[i], max_len) );
      }
    }

    return lrss;

  }

  // /**
  //  * Finds the Longest Common Substring (LCS) between a group of strings.
  //  * The current implementation takes O(nlog(n)) bounded by the suffix array construction.
  //  * @param strs - The strings you wish to find the longest common substring between
  //  * @param K - The minimum number of strings to find the LCS between. K must be at least 2.
  //  **/
  // public static TreeSet<String> lcs(String [] strs, final int K) {

  //     // CHANGE
  //     // if (K <= 1) throw new IllegalArgumentException("K must be greater than or equal to 2!");
      
  //   if (K <= 1) {
  //   	return null;
  //   }

  //   TreeSet<String> lcss = new TreeSet();
    
  //   if (strs == null || strs.length <= 1) return lcss;
    
  //   // L is the concatenated length of all the strings and the sentinels
  //   int L = 0;
    
  //   final int NUM_SENTINELS = strs.length, N = strs.length;
  //   for(int i = 0; i < N; i++) L += strs[i].length() + 1;

  //   int[] indexMap = new int[L];
  //   // CHANGE
  //   int LOWEST_ASCII = 1000;
  //   // int LOWEST_ASCII = Integer.MAX_VALUE;
  //   int k = 0;
    
  //   // Find the lowest ASCII value within the strings.
  //   // Also construct the index map to know which original 
  //   // string a given suffix belongs to.
  //   for (int i = 0; i < strs.length; i++) {
      
  //     String str = strs[i];
      
  //     for (int j = 0; j < str.length(); j++) {
  //       int asciiVal = str.charAt(j);
  //       if (asciiVal < LOWEST_ASCII) LOWEST_ASCII = asciiVal;
  //       indexMap[k++] = i;
  //     }

  //     // Record that the sentinel belongs to string i
  //     indexMap[k++] = i;

  //   }

  //   final int SHIFT = LOWEST_ASCII + NUM_SENTINELS + 1;
    
  //   int sentinel = 0;
  //   int[] T = new int[L];

  //   // CHANGE
  //   k = 0;
  //   // Construct the new text with the shifted values and the sentinels
  //   for(int i = 0; i < N; i++) {
  //   // for(int i = 0, k = 0; i < N; i++) {
  //     String str = strs[i];
  //     for (int j = 0; j < str.length(); j++)
  //       T[k++] = ((int)str.charAt(j)) + SHIFT;
  //     T[k++] = sentinel++;
  //   }

  //   // CHANGE
  //   String tmp = intArrToString(T);
  //   SuffixArray sa = new SuffixArray(tmp);
  //   // SuffixArray sa = new SuffixArray(T);
  //   Deque <Integer> deque = new ArrayDeque<>();
  //   Map <Integer, Integer> windowColorCount = new HashMap_Simple<>();
  //   Set <Integer> windowColors = new HashSet<>();
    
  //   // Start the sliding window at the number of sentinels because those
  //   // all get sorted first and we want to ignore them
  //   int lo = NUM_SENTINELS, hi = NUM_SENTINELS, bestLCSLength = 0;

  //   // Add the first color
  //   int firstColor = indexMap[sa.sa[hi]];
  //   windowColors.add(new Integer(firstColor));
  //   windowColorCount.put(new Integer(firstColor), new Integer(1));

  //   int count = 0;
    
  //   // Maintain a sliding window between lo and hi
  //   while(hi < L) {

  //     int uniqueColors = windowColors.size();
      
  //     // Attempt to update the LCS
  //     if (uniqueColors >= K) {
	
  //       // CHANGE
  //   	Integer deqPeekFirst = deque.peekFirst();
  //   	int deqPeekFirst_int = deqPeekFirst.intValue();	
  //   	int windowLCP = sa.lcp[deqPeekFirst_int];
  //   	// int windowLCP = sa.lcp[deque.peekFirst()];

  //       if (windowLCP > 0 && bestLCSLength < windowLCP) {
  //         bestLCSLength = windowLCP;
  //         lcss.clear();
  //       }

  //       if (windowLCP > 0 && bestLCSLength == windowLCP) {

  //         // Construct the current LCS within the window interval
  //         int pos = sa.sa[lo];
  //         char[] lcs = new char[windowLCP];
  //         for (int i = 0; i < windowLCP; i++) lcs[i] = (char)(T[pos+i] - SHIFT);

  //   	  // CHANGE
  //         lcss.add(new String(lcs, 0, lcs.length));
  //         // lcss.add(new String(lcs));

  //         // If you wish to find the original strings to which this longest 
  //         // common substring belongs to the indexes of those strings can be
  //         // found in the windowColors set, so just use those indexes on the 'strs' array

  //       }

  //       // Update the colors in our window
  //       int lastColor = indexMap[sa.sa[lo]];
  //   	// CHANGE
  //       Integer colorCount = windowColorCount.get(new Integer(lastColor));
  //       // Integer colorCount = windowColorCount.get(lastColor);
  // 	int check = colorCount.intValue();
  //   	// CHANGE
  //   	boolean removed = false;
  //       if (colorCount.intValue() == 1) {
  //   	    windowColors.remove(new Integer(lastColor));
  //   	    removed = true;
  //   	} 
  //   	// if (colorCount == 1) windowColors.remove(lastColor);
  //   	// CHANGE
  //       windowColorCount.put(new Integer(lastColor), new Integer(colorCount.intValue() - 1));
  //       // windowColorCount.put(lastColor, colorCount - 1);
	
  //   	// CHANGE
  //   	if (!deque.isEmpty()) {
  //   	    // CHANGE
  //   	    deqPeekFirst = deque.peekFirst();
  //   	    boolean deqPeekLessThanLo = deqPeekFirst.intValue() <= lo;
	    	    
  //   	    // Remove the head if it's outside the new range: [lo+1, hi)
  //   	    while (!deque.isEmpty() && deqPeekLessThanLo) {
  //   		deque.removeFirst();
  //   		deqPeekFirst = deque.peekFirst();
  //   		if (deqPeekFirst != null) {
  //   		    deqPeekLessThanLo = deqPeekFirst.intValue() <= lo;
  //   		} else {
  //   		    deqPeekLessThanLo = false;
  //   		}
  //   	    }

  //   	}
		
  //       // Decrease the window size
  //       lo++;

  //     // Increase the window size because we don't have enough colors
  //     } else if(++hi < L) {

  // 	int nextColor = indexMap[sa.sa[hi]];
  //   	// CHANGE 
  //   	Integer nextColor_Int = new Integer(nextColor);
	
  //       // Update the colors in our window
  //   	// CHANGE
  //       windowColors.add(nextColor_Int);
  //       // windowColors.add(nextColor);
  //   	// CHANGE
  //       Integer colorCount = windowColorCount.get(nextColor_Int);
  //       // Integer colorCount = windowColorCount.get(nextColor);
  //   	// CHANGE
  //       if (colorCount == null) colorCount = new Integer(0);
  //       // if (colorCount == null) colorCount = 0;
  //   	// CHANGE
  //       windowColorCount.put(nextColor_Int, new Integer(colorCount.intValue() + 1));
  //       // windowColorCount.put(nextColor, colorCount + 1);

  //   	// CHANGE
  //   	if (!deque.isEmpty()) {	
  //   	    // CHANGE
  //   	    Integer deqPeekLast = deque.peekLast();
  //   	    int deqPeekLast_int = deqPeekLast.intValue();	    
	    
  //   	    // CHANGE
  //   	    // Remove all the worse values in the back of the deque
  //   	    while(!deque.isEmpty() && sa.lcp[deqPeekLast_int] > sa.lcp[hi-1]) {
  //   		// while(!deque.isEmpty() && sa.lcp[deque.peekLast()] > sa.lcp[hi-1])
  //   		deque.removeLast();
  //   		// CHANGE
  //   		if (!deque.isEmpty()) {
  //   		    deqPeekLast = deque.peekLast();
  //   		    deqPeekLast_int = deqPeekLast.intValue();
  //   		}
  //   	    }
  //   	}

  //   	// CHANGE
  //       deque.addLast(new Integer(hi-1));
  //       // deque.addLast(hi-1);

  //     }
  //     count++;
  //   }

  //   return lcss;

  // }

  // // public void display() {
  // //   System.out.printf("-----i-----SA-----LCP---Suffix\n");
  // //   for(int i = 0; i < N; i++) {
  // //     int suffixLen = N - sa[i];
  // //     String suffix = new String(T, sa[i], suffixLen);
  // //     System.out.printf("% 7d % 7d % 7d %s\n", i, sa[i],lcp[i], suffix );
  // //   }
  // // }

  //   // CHANGE
  // //   // public static void main(String[] args){
  // //   harness public static void main() {      
        	
  // //   // String[] strs = { "GAGL", "RGAG", "TGAGE" };
    
  // //   String[] strs = { "AAGAAGC", "AGAAGT", "CGAAGC" };
  // //   // String[] strs = { "abca", "bcad", "daca" };
  // //   // String[] strs = { "abca", "bcad", "daca" };
  // //   // String[] strs = { "AABC", "BCDC", "BCDE", "CDED" };
  // //   // String[] strs = { "abcdefg", "bcdefgh", "cdefghi" };
  // //   // String[] strs = { "xxx", "yyy", "zzz" };
  // //   TreeSet <String> lcss = SuffixArray.lcs(strs, 2);
  // //   // System.out.println(lcss);

  // //   // SuffixArray sa = new SuffixArray("abracadabra");
  // //   // System.out.println(sa);
  // //   // System.out.println(java.util.Arrays.toString(sa.sa));
  // //   // System.out.println(java.util.Arrays.toString(sa.lcp));

  // //   // SuffixArray sa = new SuffixArray("ababcabaa");
  // //   // sa.display();
    
  

  // // }

}

