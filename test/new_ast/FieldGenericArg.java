class A<T> {
    T tt;
    T() { this.tt = new Integer(1); }
    T get (T t) { return this.tt; }
}
class B {
    A<Integer> a;
    B() { a = new A<>(); }
}

class FieldGenericArg {
    harness void mn() {
	B b = new B();
	
	assert b.a.get(new Integer(1)) != null;
    }
}
