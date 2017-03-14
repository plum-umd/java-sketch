class MethodcallScope {
    harness void mn() {
	A a = new A();
	a.x = 1;
	int r = a.m1().m0();
	assert r == 1;
    }
}

class A {
    int x;
    int m0() { return x; }
    A m1() { return this; }
    A m2() { this.x = 2; return this; }
}

class B extends A {
    A m1() { return this; }
}
