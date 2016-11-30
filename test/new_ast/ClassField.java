class A {
    int x;
}
class B {
    A a;
}
class C {
    B b;
}

class ClassField {
    harness static void test () {
	// B b = new B();
	// b.a = new A();
	// b.a.x = 1;
	C c = new C();
	cA.b = new B();
	c.b.a = new A();
	c.b.a.x = 1;
    }
}
