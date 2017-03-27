class A {
    void m() { }
}
class B {
    A a;
    B() { a = new A(); }
}
class FieldMethod {
    harness void main() {
	B b = new B();
	b.a.m();
    }
}
