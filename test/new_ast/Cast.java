class Cast {
    int m(int a) {
	double x = 1.0;
	return a * (int)x;
    }
    harness void main(int x) {
	assert m(x) == x;
    }
}
