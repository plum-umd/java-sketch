class A {
    static int static_mtd(int a, int b) { return a + b; }
}

class B extends A { }

class C { static int m() { return A.static_mtd(2 + 3, 4); } }

class StaticCalls {
    static int m() { int x = 1; int y = 2; return x + y; }
    harness void statics(int a, int b) {
	int x = m();
	assert x == 3;
	assert m() == 3;

	x = A.static_mtd(a, b);
	assert x == a +b;
	assert A.static_mtd(a, b) == a + b;

	assert B.static_mtd(a, b) == a + b;

	assert C.m() == 9;
    }
}
