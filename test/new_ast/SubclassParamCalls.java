class A {
    void m(A a) { }
}

class B extends A {
    void m(A a) { }
}
class SubclassParamCalls {
    harness void main() {
	B b = new B();
	b.m(b);
    }
}
