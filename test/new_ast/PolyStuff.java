import java.util.List;

class PolyStuff {
    harness void mn(int[] x) {
	int[] i;
	i = new int[5];
	int j = i.length;
	assert m(i) == 2*j;
    } 
    void m() {
	// A a = new A();
	// assert m(a) == A();

	// B b = new B();
	// assert m(b) == B();
    }
    <T> void m(T[] t) {
    	int a = t.length;
	for (T tt : t) { a++; }
	return a;
    }
}

// class A { }
// class B { }
