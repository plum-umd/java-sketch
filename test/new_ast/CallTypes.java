class A { }
class B extends A { }

class CallTypes {
    void m(A a) { }
	
    harness void main(int x) {
	B b = new B();
	m(b);
    }
}
