class ArrayList_test {
    harness void m() {
	ArrayList<Integer> ints = new ArrayList<Integer>();
	ArrayList<String> strs = new ArrayList<String>();
	ArrayList<Object> objs = new ArrayList<Object>();
	ArrayList<Number> nums = new ArrayList<Number>();
	
	/*
	// add, add @ index, size, contains, indexOf
	Integer n1 = new Integer(7);
	Integer n2 = new Integer(-4);
	Integer n3 = new Integer(31415);

	assert ints.size() == 0;
	assert !ints.contains(n1);

	ints.add(n1);

	assert ints.size() == 1;
	assert ints.contains(n1);
	assert !ints.contains(n2);

	ints.add(n2);

	assert ints.size() == 2;
	assert ints.contains(n2);
	assert !ints.contains(n3);

	ints.add(0, n3);
	
	assert ints.size() == 3;
	assert ints.indexOf(n3) == 0;
	assert ints.indexOf(n1) == 1;
	assert ints.indexOf(n2) == 2;

	ints.add(n3);

	assert ints.contains(n3);
	assert ints.indexOf(n3) == 0;
	assert ints.size() == 4;

	// clear, contains

	ints.clear();
	
	assert ints.size() == 0;
	assert !ints.contains(n1);
	assert !ints.contains(n2);
	assert !ints.contains(n3);

	// get, remove, remove @ index, contains, size, set
	String s1 = "String 1";
	String s2 = "String 2";
	String s3 = "String 3";
	String s4 = "String 4";

	strs.add(s1);
	strs.add(s2);
	strs.add(s3);	
	strs.add(s4);	

	assert (strs.get(0)).equals("String 1");
	assert (strs.get(1)).equals("String 2");
	assert (strs.get(2)).equals("String 3");
	assert (strs.get(3)).equals("String 4");

	strs.remove(s1);

	assert strs.size() == 3;
	assert (strs.get(0)).equals("String 2");
	assert (strs.get(1)).equals("String 3");
	assert (strs.get(2)).equals("String 4");
	assert !strs.contains(s1);

	assert (strs.remove(1)).equals("String 3");

	assert strs.size() == 2;
	assert (strs.get(0)).equals("String 2");
	assert (strs.get(1)).equals("String 4");
	assert !strs.contains(s3);

	assert (strs.set(0, s1)).equals("String 2");

	assert strs.size() == 2;
	assert (strs.get(0)).equals("String 1");
	assert (strs.get(1)).equals("String 4");
	assert !strs.contains(s2);

	// toArray
	Object[] arr = strs.toArray();
	*/
    }
}
