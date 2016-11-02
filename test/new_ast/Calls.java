class Calls {
    harness void test(int x) {
	Calls c = new Calls();
	int cf0 = c.f0;
	int cf1 = A.f1;
	// int s = Calls.setF1(5);
	// c.setF0(s);
	// c.setF0(Calls.f1);
    }
}

class A {
    int f0;
    static int f1;
    // void m0(int f0) {
    // 	int a = f0;
    // }
    // void setF0(int x) {
    // 	f0 = x;
    // }
    // static void setF1(int x) {
    // 	f1 = x;
    // }
}

class B {
    void b(int f0) {
	int bb = f0;
    }
}
