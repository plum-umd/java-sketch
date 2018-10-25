public class Arrays {

    public static SuffixRankTuple[] swap(SuffixRankTuple[] a, int i, int j) {
    // public static void swap(Object[] a, int i, int j) {
	// Object tmp = a[i];
	SuffixRankTuple tmp = a[i];

	a[i] = a[j];
	a[j] = tmp;

	return a;
    }
    
    public static SuffixRankTuple[] sort(SuffixRankTuple[] a, int n) {
    // public static void sort(Comparable[] a) {	
	// int n = a.length;
	for (int j=0; j<n-1; j++) {
	  int iMin = j;
	  for (int i=j+1; i<n; i++) {
	      SuffixRankTuple a1 = a[i];
	      SuffixRankTuple a2 = a[iMin];
	      int cmp = a1.compareTo(a2);
	      if (cmp < 0) {
	      	  iMin = i;
	      }
	  }
	  if (iMin != j) {
	      a = swap(a, j, iMin);
	  }
	}
	return a;
    }
}
