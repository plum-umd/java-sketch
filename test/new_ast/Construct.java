class F {
    int x;
    // F() { }
    void m() {
	x = 0;
    }
}

class Construct {
    harness static void test(int v) {
	F t = new F();
    }
}
