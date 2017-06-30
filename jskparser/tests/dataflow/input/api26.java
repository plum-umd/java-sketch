class A {
    void getStart(int x, int y) {
	if (x < y) {
	    return x;
	}
	else if (y == x) {
	    return null;
	}
	else {
	    return y;
	}
    }
}
