class A {
    int x;
}

class B {
    A[] alist;
    int [] x;
}

class SimpleArray {
    harness void main() {
	A a = new A();
	a.x = 1;
	B b = new B();
	b.alist = new A[] {a};
	assert b.alist[0].x == 1;
    }
}
