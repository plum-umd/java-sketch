class PolymorphicFunctions {
    harness void main() { }
    // public static <T> void m() {
    // 	T t;
    // }

    T m1(T t) {
	t = new T();
	t = new A();
    }
}

class A {}
