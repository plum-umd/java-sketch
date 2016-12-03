class A {
    int m() {
	return 1;
    }
    int m1(int x) {
    	return x + 1;
    }
    void m2() {
	int a = 0;
    }
}    
class NonLocalCalls {
    harness void main(int x) {
	A a = new A();
	int y = a.m();
	int z = a.m1(x);
	a.m2();
	assert y == 1;
	assert z == x + 1;
	assert a.m() == 1;
	assert a.m1(x) == x + 1;
    }
}
