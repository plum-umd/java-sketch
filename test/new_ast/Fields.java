class A {
    static int f1;
    int f2;
}

class Fields {
    harness static void test () {
	A.f1 = 0;

	A a = new A();
	a.f2 = 0;
    }
}
