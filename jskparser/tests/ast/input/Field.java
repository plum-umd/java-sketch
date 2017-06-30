class A {
    // static int a1;
    class B {
    }
}

class B {
    void b() {
	A a = new A();
	a.a0 = 0;
	a.a0 = A.a1;
    }
}
