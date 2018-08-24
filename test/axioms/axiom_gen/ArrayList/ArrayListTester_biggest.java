public class ArrayListTester {
    harness public void mn(int l1, int l2, int l3, int i1) {
	assume l1 >= 0 && l1 <= 10;
	assume l2 <= l1;
	assume l3 <= l1 && l3 >= 0;
	assume i1 < l1-l3 && i1 >= 0;
	
	ArrayList<Integer> a = new ArrayList<Integer>();

	for(int i = 0; i < l1; i++) {
	    Integer j = new Integer(i);
	    a.add(j);
	}

	int sz = a.size();
	assert sz == l1;

	for(int i = 0; i < l2; i++) {
	    Integer j = new Integer(i+1);
	    a.set(i, j);
	}

	sz = a.size();
	assert sz == l1;

	if (l1-l3 > 0) {
	    Integer j = a.get(i1);
	    if (i1 < l2) {
		assert j.intValue() == i1+1;
	    } else {
		assert j.intValue() == i1;
	    }
	}
    }
}
