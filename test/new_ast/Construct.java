class F {
    int x;
    void m() {
	x = 0;
    }
}

class Construct {
    harness static void test(int v) {
	F f1 = new F();
	F f2 = new F();

	f1.m();
	f2.m();

	assert f1 != f2;
    }
}
