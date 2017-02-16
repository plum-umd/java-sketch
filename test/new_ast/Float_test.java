class Float_test {
    harness void m() {
	Float a = new Float(3.123);
	Float b = new Float(5.0);
	Float c = new Float(-4.398);
	Float d = new Float(11.89897);
	Float e = new Float(11.89897);
	Float f = new Float(4.398);
	Integer i = new Integer(5);

	// floatValue 
	float x = a.floatValue();
	assert x == 3.123;

	// intValue
	assert a.intValue() == 3;
	assert d.intValue() == 11;

	// compareTo
	assert a.compareTo(b) == -1;
	assert a.compareTo(c) == 1;
	assert d.compareTo(e) == 0;

	// compare
	float xx = 1.23; float yy = 4.56;
	assert Float.compare(xx, yy) == -1;
	// FLOAT CAST CAUSES ERROR AS DOES F NOTATION
	//assert Float.compare((float)3.1415, (float)3.1415) == 0;
	//assert Float.compare((float)6.283, (float)3.1415) == 1;

	// equals
	assert !a.equals(b);
	assert !c.equals(f);
	assert !b.equals(i);
	assert d.equals(e);

	// to String
	String aString = a.toString();

	assert aString.length() == 4;
	assert aString.equals("3.12");
    }
}
