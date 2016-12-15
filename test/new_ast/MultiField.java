class A {
    int x, y;
    void set(int a, int b) {
	x = a;
	y = b;
    }
}
class MultiField {
    harness void main() {
	A a = new A();
	a.set(1,2);
	assert a.x == 1;
	assert a.y == 2;
	
    }
}
