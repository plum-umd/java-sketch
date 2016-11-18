class This {
    harness static void mn(int x) {
	// A a = new A();
	// a.setX(x);
	// assert a.x == x;
	B a = new B();
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

class B extends A {
    void setX(int x) {
	this.x = x;
    }
}
