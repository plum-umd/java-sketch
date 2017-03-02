// class A {
//     int m() {
// 	return 1;
//     }
//     int m1(int a) {
//     	return a + 1;
//     }
//     void m2() {
// 	int a = 1;
//     }
// }
// class B extends A {
//     int m() {
// 	return 2;
//     }
// }
// class C extends B {
//     int m() {
// 	return 3;
//     }
//     int m1() {
// 	return 4;
//     }
//     int m1(int a) {
// 	return a + 2;
//     }
// }
class A {
    boolean equals(Object o) { return false; }
}
class C1 {

    public boolean arg(A o) {
	boolean b = o.equals(this);
    	if (!b) {
    	    // System.out.println("not overriden");
    	    return false;
    	}
    }

}

class C2 extends A {
    public boolean equals(Object o) {
    	// System.out.println("I AM OVERRIDDEN");
    	return true;
    }
}

    class Override {
    // public static void main(String[] args) {
    harness void main(int x) {
	C2 c2 = new C2();
	// c2.equals(c2);
	C1 c1 = new C1();
	c1.arg(c2);
	// A a = new A();
	// B b = new B();
	// int y = b.m();
	// int z = b.m1(x);
	// assert y == 2;
	// assert z == x + 1;
	// assert a.m() == 1;
	// assert a.m1(x) == x + 1;

	// C c = new C();
	// // int i = c.m1();
	// int j = c.m1(x);
	// assert j == x + 2;
    }
}
