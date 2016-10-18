class Calls {
    int f0;
    static int f1;
    int m0(int x) {
	return ?? - 1;
    }
    void setF0(int x) {
	f0 = x;
    }
    static void setF1(int x) {
	f1 = x;
    }
    harness int test(int x) {
	setF0(x);
    }
}

class A {
    void a() {
	int s = Calls.setF1(5);
	Calls c = new Calls();
	c.setF0(s);
	c.setF0(Calls.f1);
    }
}
