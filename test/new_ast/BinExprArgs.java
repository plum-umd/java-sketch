class BinExpArgs {
    int m(int a) {
	return a * -1;
    }
    harness void main() {
	int x = 1;
	int y = 2;
	int z = m(y-x);
    }
}
