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

	assert b.m(a) == 5;
    }
    
}
