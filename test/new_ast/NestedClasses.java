//  class A {
//     int f;
// }
// class B extends A { }

// class Out {
//     int f_out;
//     class In {
// 	// int f_in;
// 	void inner_m0() {
// 	//     f_in = x + 1;
// 	    f_out = x + 2;
// 	}
//     }
//     void outer_m0() {
// 	// In in = new In();
// 	// in.inner_m0(2);
// 	// in.outer_m0();
// 	// assert in.f_in == 3;
// 	// in.f_out = 2;
// 	// f_out = 2;
//     }
// }

class Outer {
    int a;
    class Inner {
	class Inner_Inner {
	    void m() {
		a = 0;
	    }
	}
    }
}

// class B extends A {
//     void m() { a = 0; }
// }

class NestedClasses {
    // int a;
    harness void main() {
	// A aa = new A();
	// aa.a = 0;
	// a = 1;
	// a = 0; // a_Inners = 0;
	// Out o = new Out();
	// o.outer_m0();
	// assert o.f_out == 2;
    }
}
