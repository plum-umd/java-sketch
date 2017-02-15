class A {
    int x;
    harness void m(int num) {
	String x = "I am a string";

	// charAt
	assert x.charAt(3) == 'm';

	// length
	assert x.length() == 13;

	// equals
	assert x.equals("I am a string") == 1;

	// concat
	String y = " concat";
	String con = x.concat(y);
	assert con.equals("I am a string concat") == 1;

	// indexOf (chars)
	assert con.indexOf('I', 0) == 0;
	assert con.indexOf('s') == 7;
	assert con.indexOf('I', 1) == -1;
	assert con.indexOf('a', 0) == 2;
	assert con.indexOf('c') == 14;
	assert con.indexOf('a', 4) == 5;
	assert con.indexOf('a', 6) == 18;

	// indexOf (strings)
	assert x.indexOf("hello", 0) == -1;
	assert x.indexOf("I", 0) == 0;
	assert x.indexOf("am", 0) == 2;
	assert x.indexOf("string", 0) == 7;
	assert x.indexOf("am", 3) == -1;
    }
}
