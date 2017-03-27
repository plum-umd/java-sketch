class B {
    int a;
    void m() {
	int a;
	a = 0;
	int x = a + 2;
    }
}

class Creation {
    void m() {
	B b = new B();
    }
}
