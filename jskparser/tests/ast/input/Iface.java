interface I {
    int m();
}
class A implements I {
    int m(I i) {
	return 1;
    }
}
class Iface {
    public static void main() {
	I a = new A();
	a.m(a);
    }
    
}
