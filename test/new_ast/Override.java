class A {
    boolean equals(Object o) { return false; }
}

class Override {
    // public static void main(String[] args) {
    harness void main(int x) {
	Object a = new A();
	Object b = new A();
	a.equals(b);
    }
}
