class String_test {
    int x;
    harness void m(int num) {
	String x = "I am a string";
	Float y = new Float(3.1415);
	Integer z = new Integer(3);

	// charAt
	assert x.charAt(3) == 'm';
	assert x.charAt(0) == 'I';

	// length
	assert x.length() == 13;

	// toString
	String s = x.toString();
	assert x == s;
	assert x.equals(s);

	// equals
	assert x.equals("I am a string");
	assert !x.equals("I am a strin");
	assert !x.equals("I am a String");
	assert !x.equals("fork");
	assert !x.equals(y);
	assert !x.equals(z);

	// concat
	String c = " concat";
	String con = x.concat(c);

	assert con.equals("I am a string concat");

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

	// replace
	String s0 = "Hello, world!";
	String s1 = s0.replace('e', 'z');
	assert s1.equals("Hzllo, world!");
	String s2 = s0.replace('a', 'z');
	assert s2.equals("Hello, world!");

	// substring_int
	String xs = x.substring(1);
	assert xs.equals(" am a string");
	xs = xs.substring(3);
	assert xs.equals(" a string");

    	// substring_int_int
	xs = x.substring(1, 5);
	assert xs.equals(" am ");
	xs = x.substring(3, 13);
	assert xs.equals("m a string");

	// split
	String ss = "This is";
	String[] sa = ss.split(" ");
	assert sa[0].equals("This");
	assert sa[1].equals("is");

    	String ss1 = "This,is,split,by, comma";
	String[] sa1 = ss1.split(",");
	assert sa1[0].equals("This");
	assert sa1[1].equals("is");
	assert sa1[2].equals("split");
	assert sa1[3].equals("by");
	assert sa1[4].equals(" comma");
    }
}
