class ThisCalls {
    harness static void mn() {
    }
}

class A {
    int ma() { return 1; }
}

class B {
    A a;
    int mb() {
	this.a = new A();
	return this.a.ma();
    }
}
