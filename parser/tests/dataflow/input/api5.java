class C {
    int m() {
	int x = 0;
	int y = x;
	x = y;
	y = x;
	return y;
    }
}
