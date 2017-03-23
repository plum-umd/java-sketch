class HashMap_add_remove {
    harness void m() {
	Map<String, Integer> m = new HashMap_Simple<String, Integer>();
	String s1 = "1";
	String s2 = "2";
	Integer i2 = new Integer(2);
	m.put(s1, i2);
	m.put(s2, i2);
	assert m.containsKey(s1);
    }
}
