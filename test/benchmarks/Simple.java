interface I { int m(); }

abstract class  A implements I {
    int m() { return 0; }
}

class B extends A {
    @Override
    int m() { return 1; }
}

class C extends A {
    @Override
    int m() { return 2; }
}

class Simple {
    harness static void m() {
	I a = new B();
    	int x = a.m();
    }
}
