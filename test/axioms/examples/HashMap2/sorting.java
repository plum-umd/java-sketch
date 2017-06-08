public class sorting {

	public ArrayList<Integer> SelectionSort(ArrayList<Integer> l) {
	    int size = l.size();
	    for (int j=0; j<size-1; j++) {
		int iMin = j;
		Integer int2, int1;
		for (int i=j+1; i<size; i++) {
		    int1 = l.get(i);
		    int2 = l.get(iMin);
		    int i1 = int1.intValue();
		    int i2 = int2.intValue();
		    if (i1 < i2) {
			iMin = i;		
		    }		    
		}
		if (iMin != j) {
		    // Integer minI = l.get(iMin);
		    // Integer atJ = l.get(j);
		    // l.remove(iMin);
		    // l.add(iMin, atJ);
		    // l.remove(j);
		    // l.add(j, minI);
		    l = swap(l, iMin, j);
		}
	    }
	    return l;
	}


    public ArrayList<Integer> swap(ArrayList<Integer> l, int i, int j) {
	Integer atI = l.get(i);
	Integer atJ = l.get(j);
	l.remove(i);
	l.add(i, atJ);
	l.remove(j);
	l.add(j, atI);

	return l;
    }
	// public ArrayList<Integer> BubbleSort(ArrayList<Integer> l) {
	//     if (l.isEmpty()) {
	// 	return l;
	//     } else {
	// 	int size = l.size();
	// 	boolean swapped = false;
	// 	boolean begin = true;
	// 	while(swapped || begin) {
	// 	    begin = false;
	// 	    for (int i=0; i<size-1; i++) {
	// 		Integer int1 = l.get(i);
	// 		Integer int2 = l.get(i+1);
	// 		int i1 = int1.intValue();
	// 		int i2 = int2.intValue();
	// 		if (i1 < i2) {
	// 		    l.remove(i+1);
	// 		    l.add(i, int2);
	// 		    swapped = true;
	// 		}
	// 	    }
	// 	}
	// 	return l;
	//     }
	// }

	public ArrayList<Integer> QuickSort(ArrayList<Integer> l) {
	    if (l.isEmpty()) {
		return l;
	    } else {
		int size = l.size();
		return QuickSort_help(l, 0, size-1);
	    }
	}

    int p = 0;

    public ArrayList<Integer> QuickSort_help(ArrayList<Integer> l, int lo, int hi) 
    {
	if (lo < hi) {
	    l = partition(l, lo, hi);
	    l = QuickSort_help(l, lo, p-1);
	    l = QuickSort_help(l, p+1, hi);
	}
	return l;
    }

    public ArrayList<Integer> partition (ArrayList<Integer> l, int lo, int hi) {
	Integer pivot = l.get(hi);
	int pivot_int = pivot.intValue();
	int i = lo - 1;
	for (int j=lo; j<hi; j++) {
	    Integer val = l.get(j);
	    int val_int = val.intValue();
	    if (val_int <= pivot_int) {
		i++;
		if (i != j) {
		    int s1 = {| i,j,val_int,pivot_int,hi,lo,p|};
		    int s2 = {| i,j,val_int,pivot_int,hi,lo,p|};
		    // l = swap(l, i, j);
		    l = swap(l, s1, s2);
		}
	    }
	}
	l = swap(l, i+1, hi);
	p = i+1;
	return l;
    }

	public boolean arrayListEquals(ArrayList<Integer> a1, ArrayList<Integer> a2) {
		if (a1 == null && a2 == null) {
			return true;
		} else if (a1 == null || a2 == null) {
			return false;
		} else {
			if (a1.size() != a2.size()) {
				return false;
			} else {
				int size = a1.size();
				for (int i=0; i < size; i++) {
					Integer i1 = a1.get(i);
					Integer i2 = a2.get(i);
					if (!(i1.equals(i2))) {
						return false;
					}
				}
				return true;
			}
		}
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

		ArrayList<Integer> r1 = SelectionSort(l1);
		ArrayList<Integer> r2 = QuickSort(l2);		
		assert arrayListEquals(r1, l3); 
		assert arrayListEquals(r2, l3); 
		assert arrayListEquals(r1, r2); 

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

		r1 = SelectionSort(l1);
		r2 = QuickSort(l2);
		assert arrayListEquals(r1, l3); 
		assert arrayListEquals(r2, l3); 
		assert arrayListEquals(r1, r2); 

	}


}
