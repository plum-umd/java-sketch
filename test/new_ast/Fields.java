class A {
    static int f1;
    int f2;
    static int m1(int a, int b) {
	return f1;
    }
    void callm1(int x) {
	x = m1(f2, x);
    }
}

class Fields {
    harness static void test () {
	A.f1 = 0;

	A a = new A();
	a.f2 = 0;
	int x = a.m1();
	a.callm1(0);
    }
}
