class PolymorphicFunctions {
    harness void main() {
	Integer o = new Integer();
	m(o);
	String s = new String();
	m(s);
    }
    <T> void m(T t) { }
    // private <T> T m1(T t) { return t; }
}
