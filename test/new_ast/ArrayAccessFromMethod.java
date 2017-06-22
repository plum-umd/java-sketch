class ArrayAccessFromMethod {
    harness void mn() {
	A a = new A();
	K k = a.keys()[0];
	assert k.equals(new Integer(0));
    }
}

class A {
    public K[] keys() {
        K[] keys = (K[]) new Object[5];
	for (int i = 0; i < 5; i++) { keys[i] = new Integer(i); }
        return keys;
    }
}
