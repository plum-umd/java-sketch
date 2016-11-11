class A {
    int ABf1;
    int Af1;
    static int x;

    void m0() {}
}
class B extends A {
    int ABf1;
    int Bf1;
    static int SAf1;

    void m0() {}
}
class Fields {
    harness static void test () {
	A.x = 1;
	int z = A.x;
	A a = new A();
	a.ABf1 = 1;
	a.Af1 = 2;

	B b = new B();
	b.ABf1 = 3;
	b.Bf1 = 4;
	B.SAf1 = 5;
	
	assert z == A.x;
	assert a.ABf1 == 1;
	assert a.Af1 == 2;

	assert b.ABf1 == 3;
	assert b.Bf1 == 4;
	assert B.SAf1 == 5;
	assert b.SAf1 == 5;
	assert b.x == 1;
    }
}
