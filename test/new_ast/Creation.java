class A {
    int x;
    void setX(int a) {
	x = a;
    }
    int getX() {
	return x;
    }
}

class Creation {
    harness void test () {
	A a = new A();
	a.setX(1);
	assert a.getX() == 1;
    }
}
