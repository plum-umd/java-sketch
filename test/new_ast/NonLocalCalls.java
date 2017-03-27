interface I { int i(); }
class A implements I {
    int i() { return 5; }
    int mA() { return 1; }
    int mAA() { return 4; }
    int m1(int x) {
    	return x + 1;
    }
    void m2() {
    	int a = 0;
    }
}
class B extends A {
    int mA() { return 2; }
    int mB() { return 3; }
}
class C extends B {

}

class NonLocalCalls {
    harness void main(int x) {
	A a = new A();
	int y = a.mA();
	assert y == 1;

	B b = new B();
	y = b.mA();
	assert y == 2;
        assert b.mB() == 3;
	assert b.mAA() == 4;

	C c = new C();
	assert c.mA() == 2;
	int z = a.m1(x);
	assert z == x + 1;
	assert a.m1(x) == x + 1;
	a.m2();

	I ii = new A();
	assert ii.i() == 5;
    }
}
