class Axiom_String {
    harness void mn() {
	test_7_6();
	// test_100_200();
    }

    void test_7_6() {
    	String s1 = "hello, ";
    	String s2 = "world!";
	String s3 = s1.concat(s2);
	int len12 = s1.length() + s2.length();
	int len3 = s3.length();
	assert len3 == len12;
    }
    void test_100_200() {
    	String s1 = "0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789";
    	String s2 = "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789";
	String s3 = s1.concat(s2);
	int len12 = s1.length() + s2.length();
	int len3 = s3.length();
	assert len3 == len12;
    }
}
