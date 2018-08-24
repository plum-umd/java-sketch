public class ArrayListTester {
    harness public void mn(int l) {
	assume l >= 0;

	ArrayList<Integer> a = new ArrayList<Integer>();

	for(int i = 0; i < l; i++) {
	    Integer j = new Integer(i);
	    a.add(j);
	}

	int sz = a.size();

	assert sz == l;
    }
}
