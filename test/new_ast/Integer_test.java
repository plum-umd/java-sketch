class A {
    int x;
    harness Integer m(int num) {
	Integer n = new Integer(num);
	/*
	Integer y = new Integer(0);
	int comp = n.compareTo(y);
	Integer ret = new Integer(0);
	Integer obj = new Integer(1234);
	int v = 2;

	this.x = n.intValue();
	if (comp < 0) {
	    return ret;
	} else if (comp > 0) {
	    return y;
	}

	// PARSING ERROR ???
	int a = y.equals(ret);
	int b = obj.equals(y);

	assert a == 1;
	assert b == 0;


	String str = obj.toString();
	String str2 = y.toString();

	assert str.length() == 4;
	// BOOLEAN RETURN DOESN"T PARSE RIGHT!
	assert str.equals("1234") == 1;
	assert str2.equals("0") == 1;
	*/
	return n;
    }
}
