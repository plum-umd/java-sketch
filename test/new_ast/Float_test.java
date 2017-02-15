class A {
    float x;
    harness Integer m(float num) {
	Float n = new Float(num);
	Float a = new Float(3.123);
	Float b = new Float(5.0);
	Integer c = new Integer(5);

	int comp = a.compareTo(b);

	assert comp == -1;
	assert a.equals(b) == 0;
	assert b.equals(c) == 0;
	assert b.intValue() == 5;

	String aString = a.toString();

	//assert aString.length() == 4;
	//assert aString.equals("3.12") == 1;

	return n;
    }
}
