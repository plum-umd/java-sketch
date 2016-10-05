class A {
    static int x;
    int y;
    static int m0() {
	x = 0;
	return x;
    }
    int m1() {
	x = 1;
	y = 1;
	A.x = 1;
	return y;
    }
}

class Calls {
    harness static void test () {
	int v0 = A.m0();
	A a = new A();
	int v1 = a.m1();
    }
}
