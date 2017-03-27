class A {
    int m(int x) { return x + 1; }
}
class B extends A {
    int m1(int x) { return super.m(x); }
}
class SuperCalls {
    harness void main(int x) {
	B b = new B();
	assert b.m1(x) == x + 1;
    }
}
