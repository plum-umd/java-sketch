class A {
    int buf;
    void setCharAt(int i, char c) {
	// this.buf.setCharAt(i, c);
    }
}

class Args {
    harness void main () {
	A a = new A();
	a.setCharAt(0, 'h');
    }
}
