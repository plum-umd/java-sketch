class A {
    static int f1;
    int f2;
    public void setf1(int a) {
	f1 = a;
    }
}

class Fields {
    harness static void test () {
	A a = new A();
	int x = 0;
	if (x == 0) {
	    a.setf1(0);
	}
	else {
	    a.setf1(1);
	}
	a.f2 = A.f1;
	assert a.f2 == A.f1;
	assert A.f1 == 0;
    }
}
