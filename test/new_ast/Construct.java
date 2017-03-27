class F {
    int x;
    void m() {
	x = 0;
    }
}

class A {
    int x;
    A(int x) { this.x = x; }
}

class Construct {
    harness static void test(int v) {
	A a = new A(1);
	
	F f1 = new F();
	F f2 = new F();

	f1.m();
	f2.m();

	assert f1 != f2;
    }
}
