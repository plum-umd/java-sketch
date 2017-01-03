class C {
    void m() {
	int[] x;
	x = new int[5];
	for (int i = 1; i < 5; i++) {
	    x[i] = x[i-1] + 1;
	}
	return x;
    }
}
