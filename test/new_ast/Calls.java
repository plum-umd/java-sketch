class A {
    int f;
    static int sb(int a, int b) {
    	return a + b;
    }
    void pb(int x) {
	f = x + 1;
    }
    int ab() {
    	return 3;
    }
    int ab(int a) {
    	return a;
    }
}

class B {
    int f;
    int f2;
    static int sb(int a, int b) {
    	return a + b;
    }
    void pb() { f = 1; }
    void pb(int x) {
    	f = x;
    }
    int bb() {
    	return 2;
    }
    void bf() {
    	f = 1;
    }
}

class C extends B {
    int f1;
    void pb(int x) {
    	f1 = x;
    }
}
class Calls {
    // harness void test(int x) {
    public static harness void main(int x) {
	A a = new A();
	int r1 = A.sb(5, x);
	assert r1 == 5 + x;
	a.pb(x);
	assert a.f == x + 1;
	// method overloading
	assert a.ab() == 3;
	assert a.ab(x) == x;


    	B b = new B();
    	// static call
    	assert B.sb(1, x) == 1 + x;
    	// pb in overridden in B
    	b.pb(x);
    	assert b.f == x;
    	assert b.bb() == 2;

    	C c = new C();
    	// check if subclass method is called
    	c.pb(x);
    	assert c.f1 == x;
    	c.pb();
    	assert c.f == 1;
    	// method only in super class
    	assert c.bb() == 2;
    	// static methods
    	assert B.sb(x, x) == x+x;
    	assert c.sb(x, x) == x+x;
    	assert C.sb(x, x) == 2*x;
    	c.bf();
    	assert c.f == 1;

    	B bc = new C();
    	bc.pb(x + 1);
    	assert bc.f1 == x + 1;
    	assert bc.bb() == 2;
    }
}
