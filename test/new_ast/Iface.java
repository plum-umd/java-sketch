interface I {
    int m();
}
class A implements I {
    int m() { return 1; }
}

class B implements I {
    int m() { return 2; }
    int m1(I i) { return 5; }
}

class C extends B {
    int m() { return 3; }
}
class D extends C {
    int m() { return 4; }
}

class Iface {
    harness void main() {
	I a = new A();
	I b = new B();
	I c = new C();
	I d = new D();

	assert a.m() == 1;
	assert b.m() == 2;
	assert c.m() == 3;
	assert d.m() == 4;

	assert b.m1(a) == 5;
    }
    
}
