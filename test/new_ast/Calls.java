class A {
    int m0() {
	return 0;
    }
}

class Calls {
    void a() { }
    harness static void test () {
	// a();
	A a = new A();
	int x = a.m0();
    }
}
