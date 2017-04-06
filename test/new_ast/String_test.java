class String_test {
    int x;
    harness void m(int num) {
	// String x = "I am a string";
	// Float y = new Float(3.1415);
	// Integer z = new Integer(3);

	// // charAt
	// assert x.charAt(3) == 'm';
	// assert x.charAt(0) == 'I';

	// // length
	// assert x.length() == 13;

	// // toString
	// String s = x.toString();
	// assert x == s;
	// assert x.equals(s);

	// // equals
	// assert x.equals("I am a string");
	// assert !x.equals("I am a strin");
	// assert !x.equals("I am a String");
	// assert !x.equals("fork");
	// assert !x.equals(y);
	// assert !x.equals(z);

	// // concat
	// String c = " concat";
	// String con = x.concat(c);

	// assert con.equals("I am a string concat");

	// // indexOf (chars)
	// assert con.indexOf('I', 0) == 0;
	// assert con.indexOf('s') == 7;
	// assert con.indexOf('I', 1) == -1;
	// assert con.indexOf('a', 0) == 2;
	// assert con.indexOf('c') == 14;
	// assert con.indexOf('a', 4) == 5;
	// assert con.indexOf('a', 6) == 18;

	// // indexOf (strings)
	// assert x.indexOf("hello", 0) == -1;
	// assert x.indexOf("I", 0) == 0;
	// assert x.indexOf("am", 0) == 2;
	// assert x.indexOf("string", 0) == 7;
	// assert x.indexOf("am", 3) == -1;

	// replace
	String s0 = "Hello, world!";
	String s1 = s0.replace('e', 'z');
	assert s1.equals("Hello, world!");
    }
}
