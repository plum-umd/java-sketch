class A {
    int ABf1;
    int Af1;
    static int x;
}
class B extends A {
    int ABf1;
    int Bf1;
    static int SAf1;
}
class Fields {
    static int F;
    harness static void test () {
	F = 0;
	A.x = 1;
	int z = A.x;
	A.x = A.x;
	A a = new A();
	a.ABf1 = 1;
	a.Af1 = 2;

	assert z == A.x;
	assert a.ABf1 == 1;
	assert a.Af1 == 2;

	B b = new B();
	b.Af1 = 6;
	b.ABf1 = 3;
	b.Bf1 = 4;
	B.SAf1 = 5;

	assert b.Af1 == 6;
	assert b.ABf1 == 3;
	assert b.Bf1 == 4;
	assert B.SAf1 == 5;
	assert b.SAf1 == 5;
	assert b.x == 1;
    }
}
