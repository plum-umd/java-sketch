class StaticVars {
    harness void main(int x) {
    	m(x);
    	assert A.x == x;
	assert A.c[0] == '1';
    }
    static void m(int x) {
    	A.m();
    	assert A.x == 5;
    	A.x = x;
    }
}

class A {
    static int x;
    static char[5] c = {'1'};
    static void m() {
    	this.x = 5;
    }
}
