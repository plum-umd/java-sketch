public class sorting2 {

	// generator public ArrayList<Integer> swapVals(ArrayList<Integer> l, int i, int j, int n) {
	public ArrayList<Integer> swapVals(ArrayList<Integer> l, int i, int j, int n) {		
		Integer atI = l.get(i);
		Integer atJ = l.get(j);
		int iVal = atI.intValue();
		int jVal = atJ.intValue();
		if (jVal < iVal) {
		// if ({|iVal < jVal, iVal > jVal|}) {
			l = swap(l, i, j, atI, atJ, n);
		}		
		return l;
	}

	public ArrayList<Integer> sorting1(ArrayList<Integer> l, int n) {
		int i1 = 0;
		int i2 = 0;
		while(i1 < {| n, n-1 |}) {
			// i2 = i1 + ??;
			// assert i2 < n;
			i2 = i1 + 1;
			while(i2 < {| n, n-1 |}) {				
				l = swapVals(l, i1, i2, n);
				i2++;
			}
			// l = swapVals(l, i1, i2, n);
			i1++;
		}

		return l;
		// while (i1 < n-1) {
		// 	i2 = i1 + 1;
		// 	while (i2 < n) {
		// 		l = swapVals(l, i1, i2, n);
		// 		i2++;
		// 	}
		// 	i1++;
		// }
		// return l;
	}

	public boolean testSorted(ArrayList<Integer> l, int n) {
		Integer v1, v2;
		if (n == 0) {
			return true;
		} else {
			v1 = l.get(0);
		}
		for(int i = 1; i < n; i++) {
			v2 = l.get(i);
			int val1 = v1.intValue();
			int val2 = v2.intValue();
			if (val2 < val1) {
				return false;
			}
			v1 = v2; 
		}
		return true;
	}

	harness public static void main() {
		ArrayList<Integer> l1 = new ArrayList<Integer>();
		ArrayList<Integer> l2 = new ArrayList<Integer>();
		ArrayList<Integer> l3 = new ArrayList<Integer>();
		ArrayList<Integer> l4 = new ArrayList<Integer>();
		Integer i1 = new Integer(55);
		Integer i2 = new Integer(15);
		Integer i3 = new Integer(45);
		Integer i4 = new Integer(25);
		Integer i5 = new Integer(85);
		l1.add(i1);
		l1.add(i2);
		l1.add(i3);
		l1.add(i4);
		l1.add(i5);

		l2.add(i1);
		l2.add(i2);
		l2.add(i3);
		l2.add(i4);
		l2.add(i5);

		l3.add(i2);
		l3.add(i4);
		l3.add(i3);
		l3.add(i1);
		l3.add(i5);

		l4.add(i1);
		l4.add(i2);
		l4.add(i3);
		l4.add(i4);
		l4.add(i5);

		ArrayList<Integer> r1 = sorting1(l1, 5);
		assert testSorted(r1, 5); 

		l1.clear();
		l2.clear();
		l3.clear();

		Integer i6 = new Integer(678);
		Integer i7 = new Integer(476);
		Integer i8 = new Integer(277);
		Integer i9 = new Integer(113);
		Integer i10 = new Integer(13);

		l1.add(i6);
		l1.add(i7);
		l1.add(i8);
		l1.add(i9);
		l1.add(i10);

		l2.add(i6);
		l2.add(i7);
		l2.add(i8);
		l2.add(i9);
		l2.add(i10);

		l3.add(i10);
		l3.add(i9);
		l3.add(i8);
		l3.add(i7);
		l3.add(i6);

		r1 = sorting1(l1, 5);
		assert testSorted(r1, 5); 
	}

	public ArrayList<Integer> swap(ArrayList<Integer> l, int i, int j, Integer atI, Integer atJ, int n) {
		assume i < n;
		assume j < n;
		// assert i < n;
		// assert j < n;
		l.remove(i);
		l.add(i, atJ);
		l.remove(j);
		l.add(j, atI);

		return l;
	}
}