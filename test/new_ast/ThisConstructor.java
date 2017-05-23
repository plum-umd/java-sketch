class A {
    public int x;
    public A() { this(10); }
    public A(int x) { this.x = x; }
}

class ThisConstructor {
    harness void mn() {
	A a = new A();
	assert a.x == 10;
    }
}
