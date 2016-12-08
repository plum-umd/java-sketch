class A {
    int m() {
	return 1;
    }
    int m1(int a) {
    	return a + 1;
    }
    void m2() {
	int a = 1;
    }
}
class B extends A {
    int m() {
	return 2;
    }
}
class C extends B {
    int m() {
	return 3;
    }
    int m1() {
	return 4;
    }
    int m1(int a) {
	return a + 2;
    }
}
class Override {
    harness void main(int x) {
	A a = new A();
	B b = new B();
	int y = b.m();
	int z = b.m1(x);
	assert y == 2;
	assert z == x + 1;
	assert a.m() == 1;
	assert a.m1(x) == x + 1;

	C c = new C();
	// int i = c.m1();
	int j = c.m1(x);
	assert j == x + 2;
    }
}
