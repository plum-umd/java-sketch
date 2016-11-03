class A {
    int Af1;
    void m0() {}
    // int f3, f4;
    // static int f5;
    // int f6;
    // public void setf1(int a) {
    // 	f1 = a;
    // }
}
class B extends A {
    int Af1;
    int Bf1;
    void m0() {}
}
class Fields {
    harness static void test () {
	A a = new A();
	// int x = 0;
	// if (x == 0) {
	//     a.setf1(0);
	// }
	// else {
	//     a.setf1(1);
	// }
	// a.f3 = A.f1;
	// assert a.f2 == A.f1;
	// assert A.f1 == 0;
    }
}
