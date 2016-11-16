class This {
    harness static void mn(int x) {
	A a = new A();
	a.setX(x);
	assert a.x == x;
    }
}

class A {
    int x;
    void setX(int x) {
	this.x = x;
    }
}
