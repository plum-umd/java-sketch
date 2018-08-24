public class ArrayListTester {
    harness public void mn(int l1, int l2, int l3) {
	assume l1 >= 0 && l1 <= 10;
	assume l2 <= l1;
	assume l3 <= l1;
	
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

	for(int i = l3; i > 0; i--) {
	    a.remove(i);
	}

	sz = a.size();
	assert sz == l1-l3;
    }
}
