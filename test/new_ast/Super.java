class A {
    int x;
    A(int y) {
	x = y;
    }
}

class B extends A {
    B(int v) {
	super(v);
    }
    
}

class Super {
    harness void sup() {
	A a = new A();
    }
}
