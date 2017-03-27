class This {
    harness static void mn(int z) {
	A a = new A();
	a.setX(z);
	assert a.x == z;
	B b = new B();
	b.setX(z);
	assert b.x == z;
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
