public class TreeSetTester {
    // harness public void mn() {    
    harness public void mn(int l1, int l2, int i1, int i2, int i3, int i4) {
    	assume l1 >= 0 && l1 <= 5;
    	assume l2 < l1;
	assume i1 >= 0 && i1 < l1;
	assume i2 >= 0 && i2 < l1;
	assume i3 >= 0 && i3 < l1;
	assume i4 >= 0 && i4 < l1;	
	// int l1 = 5;
	// int l2 = 2;
	
	TreeSet<Integer> t = new TreeSet<Integer>();

	for(int i=0; i<l1; i++) {
	    if (i == l2) {
		t.clear();
	    }
	    Integer j = new Integer(i);
	    t.add(j);
	    if (i == i2 || i == i3 || i == i4) {
		t.add(j);
	    }	    
	}

	int sz = t.size();
	assert sz == l1 - l2;
	
	Integer k = new Integer(i1);
	boolean b = t.contains(k);
	
	if (i1 >= l2) {
	    assert b;	    
	} else {
	    assert !b;
	}
    }
}
