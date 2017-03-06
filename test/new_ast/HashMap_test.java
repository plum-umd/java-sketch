class HashMap_test {
    harness void m() {
	// constructors
	HashMap_Simple<Integer, Integer> hm1 = new HashMap_Simple<Integer, Integer>();
	// Integer n1 = new Integer(1);
	// Integer n2 = new Integer(2);
	// Integer n3 = new Integer(3);
	// Integer n4 = new Integer(4);

	// // isEmpty, containsKey, containsValue, size
	// assert hm1.isEmpty();
	// assert hm1.size() == 0;
	// assert !hm1.containsKey(n1);
	// assert !hm1.containsValue("One");

	// // // put
	// hm1.put(n1, "One");

	// assert hm1.size() == 1;
	// assert !hm1.isEmpty();
	// assert hm1.containsKey(n1);
	// assert hm1.containsValue("One");
	// assert !hm1.containsKey(n2);
	// assert !hm1.containsValue("Two");
	// assert !hm1.containsKey(n3);
	// assert !hm1.containsValue("Three");

	// // // put (multiple)
	// hm1.put(n2, "Two");
	// hm1.put(n3, "Three");
	
	// assert hm1.size() == 3;
	// assert hm1.containsKey(n1);
	// assert hm1.containsValue("One");
	// assert hm1.containsKey(n2);
	// assert hm1.containsValue("Two");
	// assert hm1.containsKey(n3);
	// assert hm1.containsValue("Three");

	// // // put (replace previous value)
	// hm1.put(n2, "Replaced Two");

	// assert hm1.size() == 3;
	// assert hm1.containsKey(n1);
	// assert hm1.containsValue("One");
	// assert hm1.containsKey(n2);
	// assert !hm1.containsValue("Two");
	// assert hm1.containsValue("Replaced Two");
	// assert hm1.containsKey(n3);
	// assert hm1.containsValue("Three");

	// // // get
	// String s1 = hm1.get(n1);
	// String s2 = hm1.get(n2);
	// String s3 = hm1.get(n3);
	// String s4 = hm1.get(n4);

	// assert s1.equals("One");
	// assert s2.equals("Replaced Two");
	// assert s3.equals("Three");
	// assert s4 == null;
	
	// // // remove
	// hm1.remove(n2);
	// s2 = hm1.get(n2);

	// assert hm1.size() == 2;
	// assert !hm1.containsKey(n2);
	// assert s2 == null;
	// assert hm1.containsKey(n1);
	// assert hm1.containsValue("One");
	// assert hm1.containsKey(n3);
	// assert hm1.containsValue("Three");

	// // // clear
	// hm1.clear();
	
	// assert !hm1.containsKey(n1);
	// assert !hm1.containsValue("One");
	// assert !hm1.containsKey(n3);
	// assert !hm1.containsValue("Three");

	// Big table test

	int i = 0;

	Integer nBig;
	String iStr;
	int LIMIT1 = 10;
	int LIMIT2 = 10;

	for (i = 1; i < LIMIT1; i++) {
	    nBig = new Integer(i*3);
	    iStr = nBig.toString();
	    hm1.put(nBig, iStr);
	}

	for (i = 1; i < LIMIT2; i++) {
	    nBig = new Integer(i*3);
	    iStr = nBig.toString();
	    assert hm1.containsKey(nBig);
	    assert hm1.containsValue(iStr);
	}
    }
}
