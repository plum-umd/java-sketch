class Integer_test {
    harness void m() {
	Integer x = new Integer(54);
	Integer y = new Integer(54);
	Integer z = new Integer(4);
	Integer q = new Integer(1234);
	Integer v = new Integer(-66);
	Integer t = new Integer(0);

	// OBJECT CAUSING ERROR?
	// going to leave this alone for now...not sure  how I want to deal with Object class
	//Object obj = new Object();

	// intValue
	int i = x.intValue();
	assert i == 54;

	// compareTo
	assert x.compareTo(y) == 0;
	assert x.compareTo(z) == 1;
	assert x.compareTo(q) == -1;
	assert x.compareTo(v) == 1;

	// compare
	assert Integer.compare(5, 5) == 0;
	assert Integer.compare(3, 4) == -1;
	assert Integer.compare(6, 2) == 1;

	// equals
	assert x != y;
	assert x.equals(y);
	assert !x.equals(z);
	//assert x.equals(obj) == 0;

	// toString
	String str_x = x.toString();
	String str_z = z.toString();
	String str_q = q.toString();
	String str_v = v.toString();
	String str_t = t.toString();

	assert str_x.equals("54");
	assert str_z.equals("4");
	assert str_q.equals("1234");
	assert str_v.equals("-66");
	assert str_t.equals("0");

	// // static toString
        String str1 = Integer.toString(12345);
        String str2 = Integer.toString(-8888);

	assert str1.equals("12345");
	assert str2.equals("-8888");
    }
}
