interface I {
    int m();
}
class A implements I {
    int m() { return 1; }
}

class B implements I {
    int m() { return 2; }
}

class C extends B {
    int m() { return 3; }
}

class Iface {
    harness void main() {
	I a = new A();
	assert a.m() == 1;

	I b = new B();
	assert b.m() == 2;

	I c = new C();
	assert c.m() == 3;
    }
    
}
