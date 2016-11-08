class Calls {
    public static harness void main() {
    // public static void main(String[] args) {
	A a = new A();
	A b = new B();
	// a.pb();
    }
}

class A {
    int x;
    // int f;
    // static int sb(int a, int b) {
    // 	return a + b;
    // }
    void pb() {
    }
    // int ab() {
    // 	return 3;
    // }
    // int ab(int a) {
    // 	return a;
    // }
}
class B extends A {
    void pb() { }
}
//     harness void test(int x) {
// 	B b = new C();
// 	b.bb();
// 	b.pb();
	// // static call
	// int r0 = B.sb(1, x);
	// B b = new B();
	// // call with method name from different class
	// b.pb();
	// assert b.bb() == 2;

	// int r1 = A.sb(5, x);
	// A a = new A();
	// a.pb();

	// assert b.f == 0;
	// assert r0 == 1 + x;

	// assert a.f == 1;
	// assert a.ab() == 3;
	// // method overloading
	// assert a.ab(x) == x;
	// assert r1 == 5 + x;

	// C c = new C();
	// // check if subclass method is called
	// c.pb();
	// assert c.f == 1;
	// // method only in super class
	// assert c.bb() == 2;
	// // static method from super class
	// assert c.sb(x, x) == 2*x;
	// c.bf();
	// assert c.f == 1;
//     }
// }

// class B {
//     int f;
//     static int sb(int a, int b) {
//     	return a + b;
//     }
//     void pb() {
//     	f = 0;
//     }
//     int bb() {
// 	return 2;
//     }
//     void bf() {
// 	f = 0;
//     }
// }

// class C extends B {
//     int f;
//     void pb() {
// 	f = 1;
//     }
// }
