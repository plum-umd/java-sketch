interface I {
    void m(I i);
}
class A implements I {
    void m(I i) {  }
    // public void m(A a) {  }
}
class B extends A {
    void m(I i);
}
class IfaceTypes {
    harness void main() {
	// I aI = new A();
	// A aA = new A();
	// aI.m(aI);
	// aA.m(aA);
	B b = new B();
	b.m(b);
    }
}

