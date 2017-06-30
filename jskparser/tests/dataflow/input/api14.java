class C {
    int m(int a) {
	int x, y, z;
	x = a;
        y = a;
	z = x + y;
	y = x;
	return y;
    }
}
