class LocalStaticCalls {
    static int m() {
	return 1;
    }
    // static int m1(int a) {
    // 	return a + 1;
    // }
    harness static void main(int x) {
	int a = LocalStaticCalls.m();
    }
}
