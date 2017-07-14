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

      // if (pos == 1) {
      // 	  assert ranks[0].originalIndex == 0;
      // 	  assert ranks[1].originalIndex == 1;	  
      // 	  assert ranks[2].originalIndex == 2;
      // 	  assert ranks[3].originalIndex == 3;	  
      // 	  assert ranks[4].originalIndex == 4;
      // 	  assert ranks[5].originalIndex == 5;	  
      // 	  assert ranks[6].originalIndex == 6;
      // 	  assert ranks[7].originalIndex == 7;	  
      // 	  assert ranks[8].originalIndex == 8;
      // 	  assert ranks[9].originalIndex == 9;	  
      // 	  assert ranks[10].originalIndex == 10;
      // 	  assert ranks[11].originalIndex == 11;	  
      // 	  assert ranks[12].originalIndex == 12;
      // 	  assert ranks[13].originalIndex == 13;	  
      // 	  assert ranks[14].originalIndex == 14;
      // 	  assert ranks[15].originalIndex == 15;	  
      // 	  assert ranks[16].originalIndex == 16;
      // 	  assert ranks[17].originalIndex == 17;	  
      // 	  assert ranks[18].originalIndex == 18;
      // 	  assert ranks[19].originalIndex == 19;
      // 	  assert ranks[20].originalIndex == 20;
      // 	  assert ranks[21].originalIndex == 21;	  	  
      // }
      // O(nlogn)
      // CHANGE
      // java.util.Arrays.sort(ranks);
      ranks = Arrays.sort(ranks, ranks.length);

      if (pos == 1) {
      	  assert ranks[0].originalIndex == 7;
      	  assert ranks[1].originalIndex == 14;	  
      	  assert ranks[2].originalIndex == 21;
      	  assert ranks[3].originalIndex == 0;	  
      	  assert ranks[4].originalIndex == 3;
      	  assert ranks[5].originalIndex == 10;	  
      	  assert ranks[6].originalIndex == 17;
      	  assert ranks[7].originalIndex == 1;	  
      	  assert ranks[8].originalIndex == 4;
      	  assert ranks[9].originalIndex == 8;	  
      	  assert ranks[10].originalIndex == 11;
      	  assert ranks[11].originalIndex == 18;	  
      	  assert ranks[12].originalIndex == 6;
      	  assert ranks[13].originalIndex == 20;	  
      	  assert ranks[14].originalIndex == 15;
      	  assert ranks[15].originalIndex == 2;	  
      	  assert ranks[16].originalIndex == 9;
      	  assert ranks[17].originalIndex == 16;	  
      	  assert ranks[18].originalIndex == 5;
      	  assert ranks[19].originalIndex == 19;
      	  assert ranks[20].originalIndex == 12;
      	  assert ranks[21].originalIndex == 13;	  	  
      }

      // if (pos == 2) {
      // 	  assert ranks[0].originalIndex == 7;
      // 	  assert ranks[1].originalIndex == 14;	  
      // 	  assert ranks[2].originalIndex == 21;
      // 	  assert ranks[3].originalIndex == 0;	  
      // 	  assert ranks[4].originalIndex == 3;
      // 	  assert ranks[5].originalIndex == 17;	  
      // 	  assert ranks[6].originalIndex == 10;
      // 	  assert ranks[7].originalIndex == 1;	  
      // 	  assert ranks[8].originalIndex == 8;
      // 	  assert ranks[9].originalIndex == 4;	  
      // 	  assert ranks[10].originalIndex == 18;
      // 	  assert ranks[11].originalIndex == 11;	  
      // 	  assert ranks[12].originalIndex == 6;
      // 	  assert ranks[13].originalIndex == 20;	  
      // 	  assert ranks[14].originalIndex == 15;
      // 	  assert ranks[15].originalIndex == 2;	  
      // 	  assert ranks[16].originalIndex == 9;
      // 	  assert ranks[17].originalIndex == 16;	  
      // 	  assert ranks[18].originalIndex == 5;
      // 	  assert ranks[19].originalIndex == 19;
      // 	  assert ranks[20].originalIndex == 12;
      // 	  assert ranks[21].originalIndex == 13;	  	  
      // }

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
	// if (pos == 1) {
	    // if (currSuffixRank.originalIndex == 14) assert newRank == 1;
	    // if (currSuffixRank.originalIndex == 21) assert newRank == 2;	    
	    // if (currSuffixRank.originalIndex == 0) assert newRank == 3;
	    // if (currSuffixRank.originalIndex == 3) assert newRank == 3;	    
	    // if (currSuffixRank.originalIndex == 10) assert newRank == 3;
	    // if (currSuffixRank.originalIndex == 17) assert newRank == 3;	    
	    // if (currSuffixRank.originalIndex == 1) assert newRank == 4;
	    // if (currSuffixRank.originalIndex == 4) assert newRank == 4;	    
	    // if (currSuffixRank.originalIndex == 8) assert newRank == 4;
	    // if (currSuffixRank.originalIndex == 11) assert newRank == 4;	    
	    // if (currSuffixRank.originalIndex == 18) assert newRank == 4;
	    // if (currSuffixRank.originalIndex == 6) assert newRank == 5;	    
	    // if (currSuffixRank.originalIndex == 20) assert newRank == 6;
	    // if (currSuffixRank.originalIndex == 15) assert newRank == 7;	    
	    // if (currSuffixRank.originalIndex == 2) assert newRank == 8;
	    // if (currSuffixRank.originalIndex == 9) assert newRank == 8;	    
	    // if (currSuffixRank.originalIndex == 16) assert newRank == 8;
	    // if (currSuffixRank.originalIndex == 5) assert newRank == 9;	    
	    // if (currSuffixRank.originalIndex == 19) assert newRank == 9;
	    // if (currSuffixRank.originalIndex == 12) assert newRank == 10;	    
	    // if (currSuffixRank.originalIndex == 13) assert newRank == 11;
	// }

	// CHANGE
        // suffixRanks[1][currSuffixRank.originalIndex] = newRank;

      }

      // if (pos == 1) {
      // 	  assert suffixRanks.get(1,12) == 10;
      // }
      
      // Place top row (current row) to be the last row
      suffixRanks.setRow(0, suffixRanks.getRow(1));
      // CHANGE
      // suffixRanks[0] = suffixRanks[1];

      // if (pos == 1) {
      // 	  assert suffixRanks.get(0,0) == 3;
      // 	  assert suffixRanks.get(0,1) == 4;
      // 	  assert suffixRanks.get(0,2) == 8;
      // 	  assert suffixRanks.get(0,3) == 3;
      // 	  assert suffixRanks.get(0,4) == 4;	  
      // 	  assert suffixRanks.get(0,5) == 9;
      // 	  assert suffixRanks.get(0,6) == 5;
      // 	  assert suffixRanks.get(0,7) == 0;
      // 	  assert suffixRanks.get(0,8) == 4;
      // 	  assert suffixRanks.get(0,9) == 8;	  
      // 	  assert suffixRanks.get(0,10) == 3;
      // 	  assert suffixRanks.get(0,11) == 4;
      // 	  assert suffixRanks.get(0,12) == 10;
      // 	  assert suffixRanks.get(0,13) == 11;
      // 	  assert suffixRanks.get(0,14) == 1;	  
      // 	  assert suffixRanks.get(0,15) == 7;
      // 	  assert suffixRanks.get(0,16) == 8;
      // 	  assert suffixRanks.get(0,17) == 3;
      // 	  assert suffixRanks.get(0,18) == 4;
      // 	  assert suffixRanks.get(0,19) == 9;	  
      // 	  assert suffixRanks.get(0,20) == 6;
      // 	  assert suffixRanks.get(0,21) == 2;
      // 	  assert suffixRanks.get(1,0) == 3;
      // 	  assert suffixRanks.get(1,1) == 4;
      // 	  assert suffixRanks.get(1,2) == 8;
      // 	  assert suffixRanks.get(1,3) == 3;
      // 	  assert suffixRanks.get(1,4) == 4;	  
      // 	  assert suffixRanks.get(1,5) == 9;
      // 	  assert suffixRanks.get(1,6) == 5;
      // 	  assert suffixRanks.get(1,7) == 0;
      // 	  assert suffixRanks.get(1,8) == 4;
      // 	  assert suffixRanks.get(1,9) == 8;	  
      // 	  assert suffixRanks.get(1,10) == 3;
      // 	  assert suffixRanks.get(1,11) == 4;
      // 	  assert suffixRanks.get(1,12) == 10;
      // 	  assert suffixRanks.get(1,13) == 11;
      // 	  assert suffixRanks.get(1,14) == 1;	  
      // 	  assert suffixRanks.get(1,15) == 7;
      // 	  assert suffixRanks.get(1,16) == 8;
      // 	  assert suffixRanks.get(1,17) == 3;
      // 	  assert suffixRanks.get(1,18) == 4;
      // 	  assert suffixRanks.get(1,19) == 9;	  
      // 	  assert suffixRanks.get(1,20) == 6;
      // 	  assert suffixRanks.get(1,21) == 2;
      // }
      
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

  // Runs on O(mlog(n)) where m is the length of the substring
  // and n is the length of the text.
  // NOTE: This is the naive implementation. There exists an
  // implementation which runs in O(m + log(n)) time
  public boolean contains(String substr) {

    if (substr == null) return false;
    if (substr.equals("")) return true;

    String suffix_str;
    int lo = 0, hi = N - 1;
    int substr_len = substr.length();

    while( lo <= hi ) {

      int mid = (lo + hi) / 2;
      int suffix_index = sa[mid];
      int suffix_len = N - suffix_index;

      // CHANGE
      char[] tmp = new char[T.length];      
      for (int i=0; i<T.length; i++) {
	  tmp[i] = (char) T[i];
      }

      // Extract part of the suffix we need to compare
      if (suffix_len <= substr_len) suffix_str = new String(tmp, suffix_index, suffix_len);
      else suffix_str = new String(tmp, suffix_index, substr_len);
      // CHANGE
      // if (suffix_len <= substr_len) suffix_str = new String(T, suffix_index, suffix_len);
      // else suffix_str = new String(T, suffix_index, substr_len);
       
      int cmp = suffix_str.compareTo(substr);

      // Found a match
      if ( cmp == 0 ) {
        // To find the first occurrence linear scan up/down
        // from here or keep doing binary search
        return true;
      
      // Substring is found above
      } else if (cmp < 0) {
        lo = mid + 1;

      // Substring is found below
      } else {
        hi = mid - 1;
      }

    }

    return false;

  }

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

  /**
   * Finds the Longest Common Substring (LCS) between a group of strings.
   * The current implementation takes O(nlog(n)) bounded by the suffix array construction.
   * @param strs - The strings you wish to find the longest common substring between
   * @param K - The minimum number of strings to find the LCS between. K must be at least 2.
   **/
  public static TreeSet<String> lcs(String [] strs, final int K) {

      // CHANGE
      // if (K <= 1) throw new IllegalArgumentException("K must be greater than or equal to 2!");
      
    if (K <= 1) {
    	return null;
    }

    TreeSet<String> lcss = new TreeSet();
    
    if (strs == null || strs.length <= 1) return lcss;
    
    // L is the concatenated length of all the strings and the sentinels
    int L = 0;
    
    final int NUM_SENTINELS = strs.length, N = strs.length;
    for(int i = 0; i < N; i++) L += strs[i].length() + 1;

    int[] indexMap = new int[L];
    // CHANGE
    int LOWEST_ASCII = 1000;
    // int LOWEST_ASCII = Integer.MAX_VALUE;
    int k = 0;
    
    // Find the lowest ASCII value within the strings.
    // Also construct the index map to know which original 
    // string a given suffix belongs to.
    for (int i = 0; i < strs.length; i++) {
      
      String str = strs[i];
      
      for (int j = 0; j < str.length(); j++) {
        int asciiVal = str.charAt(j);
        if (asciiVal < LOWEST_ASCII) LOWEST_ASCII = asciiVal;
        indexMap[k++] = i;
      }

      // Record that the sentinel belongs to string i
      indexMap[k++] = i;

    }

    // assert indexMap[0] == 0;
    // assert indexMap[1] == 0;
    // assert indexMap[2] == 0;
    // assert indexMap[3] == 0;    
    // assert indexMap[4] == 0;
    // assert indexMap[5] == 0;
    // assert indexMap[6] == 0;
    // assert indexMap[7] == 0;    
    // assert indexMap[8] == 1;
    // assert indexMap[9] == 1;
    // assert indexMap[10] == 1;
    // assert indexMap[11] == 1;    
    // assert indexMap[12] == 1;
    // assert indexMap[13] == 1;
    // assert indexMap[14] == 1;
    // assert indexMap[15] == 2;    
    // assert indexMap[16] == 2;
    // assert indexMap[17] == 2;    
    // assert indexMap[18] == 2;
    // assert indexMap[19] == 2;
    // assert indexMap[20] == 2;
    // assert indexMap[21] == 2;    
    
    final int SHIFT = LOWEST_ASCII + NUM_SENTINELS + 1;
    
    int sentinel = 0;
    int[] T = new int[L];

    // CHANGE
    k = 0;
    // Construct the new text with the shifted values and the sentinels
    for(int i = 0; i < N; i++) {
    // for(int i = 0, k = 0; i < N; i++) {
      String str = strs[i];
      for (int j = 0; j < str.length(); j++)
        T[k++] = ((int)str.charAt(j)) + SHIFT;
      T[k++] = sentinel++;
    }

    // assert T[0] == 134;
    // assert T[1] == 134;    
    // assert T[2] == 140;
    // assert T[3] == 134;
    // assert T[4] == 134;    
    // assert T[5] == 140;
    // assert T[6] == 136;
    // assert T[7] == 0;    
    // assert T[8] == 134;
    // assert T[9] == 140;    
    // assert T[10] == 134;
    // assert T[11] == 134;    
    // assert T[12] == 140;
    // assert T[13] == 153;
    // assert T[14] == 1;    
    // assert T[15] == 136;
    // assert T[16] == 140;
    // assert T[17] == 134;    
    // assert T[18] == 134;
    // assert T[19] == 140;    
    // assert T[20] == 136;
    // assert T[21] == 2;    
    
    // CHANGE
    String tmp = intArrToString(T);
    SuffixArray sa = new SuffixArray(tmp);
    // SuffixArray sa = new SuffixArray(T);

    // assert sa.sa[0] == 7;
    // assert sa.sa[1] == 14;	  
    // assert sa.sa[2] == 21;
    // assert sa.sa[3] == 0;	  
    // assert sa.sa[4] == 3;
    // assert sa.sa[5] == 17;	  
    // assert sa.sa[6] == 10;
    // assert sa.sa[7] == 1;	  
    // assert sa.sa[8] == 8;
    // assert sa.sa[9] == 4;	  
    // assert sa.sa[10] == 18;
    // assert sa.sa[11] == 11;	  
    // assert sa.sa[12] == 6;
    // assert sa.sa[13] == 20;	  
    // assert sa.sa[14] == 15;
    // assert sa.sa[15] == 2;	  
    // assert sa.sa[16] == 16;

    // Start the sliding window at the number of sentinels because those
    // all get sorted first and we want to ignore them
    int lo = NUM_SENTINELS, hi = NUM_SENTINELS, bestLCSLength = 0;

    // Add the first color
    int firstColor = indexMap[sa.sa[hi]];
    windowColors.add(new Integer(firstColor));
    windowColorCount.put(new Integer(firstColor), new Integer(1));

    int count = 0;
    
    // Maintain a sliding window between lo and hi
    while(hi < L) {

      int uniqueColors = windowColors.size();
      
      // Attempt to update the LCS
      if (uniqueColors >= K) {
	
        // CHANGE
    	Integer deqPeekFirst = deque.peekFirst();
    	assert deqPeekFirst != null;
    	int deqPeekFirst_int = deqPeekFirst.intValue();	
    	int windowLCP = sa.lcp[deqPeekFirst_int];
    	// int windowLCP = sa.lcp[deque.peekFirst()];

        if (windowLCP > 0 && bestLCSLength < windowLCP) {
          bestLCSLength = windowLCP;
          lcss.clear();
        }

        if (windowLCP > 0 && bestLCSLength == windowLCP) {

          // Construct the current LCS within the window interval
          int pos = sa.sa[lo];
          char[] lcs = new char[windowLCP];
          for (int i = 0; i < windowLCP; i++) lcs[i] = (char)(T[pos+i] - SHIFT);

    	  // CHANGE
          lcss.add(new String(lcs, 0, lcs.length));
          // lcss.add(new String(lcs));

          // If you wish to find the original strings to which this longest 
          // common substring belongs to the indexes of those strings can be
          // found in the windowColors set, so just use those indexes on the 'strs' array

        }

        // Update the colors in our window
        int lastColor = indexMap[sa.sa[lo]];
    	// CHANGE
        Integer colorCount = windowColorCount.get(new Integer(lastColor));
        // Integer colorCount = windowColorCount.get(lastColor);
	int check = colorCount.intValue();
	if (count == 2) assert check == 2;
	else if (count == 3) assert check == 1;
	else if (count == 5) assert check == 1;	
	else if (count == 7) assert check == 1;
	else if (count == 9) assert check == 1;	
	else if (count == 11) assert check == 1;
	else if (count == 13) assert check == 1;	
	else if (count == 15) assert check == 1;
	else if (count == 17) assert check == 1;	
	else if (count == 19) assert check == 1;
	else if (count == 22) assert check == 2;	
	else if (count == 23) assert check == 1;
	else if (count == 25) assert check == 1;	
	else if (count == 27) assert check == 1;
	else if (count == 29) assert check == 1;	
	else if (count == 31) assert check == 1;
	else if (count == 33) assert check == 1;	
	else assert 0 == 1;
    	// CHANGE
    	boolean removed = false;
        if (colorCount.intValue() == 1) {
    	    windowColors.remove(new Integer(lastColor));
    	    removed = true;
    	} 
    	// if (colorCount == 1) windowColors.remove(lastColor);
    	// CHANGE
        windowColorCount.put(new Integer(lastColor), new Integer(colorCount.intValue() - 1));
        // windowColorCount.put(lastColor, colorCount - 1);

	int loop_count = 0;
	
    	// CHANGE
    	if (!deque.isEmpty()) {
    	    // CHANGE
    	    deqPeekFirst = deque.peekFirst();
	    assert deqPeekFirst != null;
    	    boolean deqPeekLessThanLo = deqPeekFirst.intValue() <= lo;
	    	    
    	    // Remove the head if it's outside the new range: [lo+1, hi)
    	    while (!deque.isEmpty() && deqPeekLessThanLo) {
		// if (lo == 3) assert count == 2;
		int deqPeekFirstVal = deqPeekFirst.intValue();
		if (lo == 3) assert deqPeekFirstVal == 3;
		if (lo == 4) assert deqPeekFirstVal == 4;
		if (lo == 5) assert deqPeekFirstVal == 5;		
		if (lo == 6) assert deqPeekFirstVal == 6;
		if (lo == 7) assert deqPeekFirstVal == 7;
		if (lo == 8) assert deqPeekFirstVal == 8;		
		if (lo == 9) assert deqPeekFirstVal == 9;
		if (lo == 10) assert deqPeekFirstVal == 10;
		if (lo == 11) assert deqPeekFirstVal == 11;		
		if (lo == 12) assert deqPeekFirstVal == 12;
		if (lo == 14) assert deqPeekFirstVal == 14;
		if (lo == 15) assert deqPeekFirstVal == 15;		
		if (lo == 16) assert deqPeekFirstVal == 16;
		if (lo == 17) assert deqPeekFirstVal == 17;
		if (lo == 18) assert deqPeekFirstVal == 18;		
		if (lo == 19) assert deqPeekFirstVal == 19;
    		deque.removeFirst();
		loop_count++;
    		deqPeekFirst = deque.peekFirst();
    		if (deqPeekFirst != null) {
    		    deqPeekLessThanLo = deqPeekFirst.intValue() <= lo;
    		} else {
    		    deqPeekLessThanLo = false;
    		}
    	    }
	    // assert loop_count <= 1;

    	}
	
    	if (deque.isEmpty()) {
    	    // if (!removed) {
    	    // 	assert 0 == 1;
    	    // }
		
    	    if (windowColors.size() >= K) {
		// if (count == 2) assert 0 == 1;
		// else if (count == 3) assert 0 == 1;
		// else if (count == 5) assert 0 == 1;	
		// else if (count == 7) assert 0 == 1;
		// else if (count == 9) assert 0 == 1;	
		// else if (count == 11) assert 0 == 1;
		// else if (count == 13) assert 0 == 1;	
		// else if (count == 15) assert 0 == 1;
		// else if (count == 17) assert 0 == 1;	
		// else if (count == 19) assert 0 == 1;
		// else if (count == 22) assert 0 == 2;	
		// else if (count == 23) assert 0 == 1;
		// else if (count == 25) assert 0 == 1;	
		// else if (count == 27) assert 0 == 1;
		// else if (count == 29) assert 0 == 1;	
		// else if (count == 31) assert 0 == 1;
		// else if (count == 33) assert 0 == 1;	
    		// else assert 0 == 1;
    	    }
    	} 
	
        // Decrease the window size
        lo++;

      // Increase the window size because we don't have enough colors
      } else if(++hi < L) {

	int nextColor = indexMap[sa.sa[hi]];
    	// CHANGE 
    	Integer nextColor_Int = new Integer(nextColor);
	
        // Update the colors in our window
    	// CHANGE
        windowColors.add(nextColor_Int);
        // windowColors.add(nextColor);
    	// CHANGE
        Integer colorCount = windowColorCount.get(nextColor_Int);
        // Integer colorCount = windowColorCount.get(nextColor);
    	// CHANGE
        if (colorCount == null) colorCount = new Integer(0);
        // if (colorCount == null) colorCount = 0;
    	// CHANGE
        windowColorCount.put(nextColor_Int, new Integer(colorCount.intValue() + 1));
        // windowColorCount.put(nextColor, colorCount + 1);

    	// CHANGE
    	if (!deque.isEmpty()) {	
    	    // CHANGE
    	    Integer deqPeekLast = deque.peekLast();
    	    int deqPeekLast_int = deqPeekLast.intValue();	    
	    
    	    // CHANGE
    	    // Remove all the worse values in the back of the deque
    	    while(!deque.isEmpty() && sa.lcp[deqPeekLast_int] > sa.lcp[hi-1]) {
    		// while(!deque.isEmpty() && sa.lcp[deque.peekLast()] > sa.lcp[hi-1])
    		deque.removeLast();
		if (count != 21) assert 0 == 1;
    		// CHANGE
    		if (!deque.isEmpty()) {
    		    deqPeekLast = deque.peekLast();
    		    deqPeekLast_int = deqPeekLast.intValue();
    		}
    	    }
    	}

    	// CHANGE
        deque.addLast(new Integer(hi-1));
	assert hi-1 != 0;
        // deque.addLast(hi-1);

      }
      count++;
    }

    return lcss;

  }

  // public void display() {
  //   System.out.printf("-----i-----SA-----LCP---Suffix\n");
  //   for(int i = 0; i < N; i++) {
  //     int suffixLen = N - sa[i];
  //     String suffix = new String(T, sa[i], suffixLen);
  //     System.out.printf("% 7d % 7d % 7d %s\n", i, sa[i],lcp[i], suffix );
  //   }
  // }

    // CHANGE
    // public static void main(String[] args){
    harness public static void main() {      
        	
    // String[] strs = { "GAGL", "RGAG", "TGAGE" };
    
    String[] strs = { "AAGAAGC", "AGAAGT", "CGAAGC" };
    // String[] strs = { "abca", "bcad", "daca" };
    // String[] strs = { "abca", "bcad", "daca" };
    // String[] strs = { "AABC", "BCDC", "BCDE", "CDED" };
    // String[] strs = { "abcdefg", "bcdefgh", "cdefghi" };
    // String[] strs = { "xxx", "yyy", "zzz" };
    TreeSet <String> lcss = SuffixArray.lcs(strs, 2);
    // System.out.println(lcss);

    // SuffixArray sa = new SuffixArray("abracadabra");
    // System.out.println(sa);
    // System.out.println(java.util.Arrays.toString(sa.sa));
    // System.out.println(java.util.Arrays.toString(sa.lcp));

    // SuffixArray sa = new SuffixArray("ababcabaa");
    // sa.display();
    
  

  }

}

