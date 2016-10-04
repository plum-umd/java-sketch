class A {
    static int f1;
    int getf1() {
	return f1;
    }
}

class Statics {
    harness static void test () {
	A a = new A();
	a.f1 = 0;
	// int x = a.getf1();
	A.f1 = 0;
    }
}
