class Inv {

    static int h = ??;

    static boolean inv (int x, int n) {
        if (x - n <= h) {
            return true;
        } else {
            return false;
        }
    }

    harness static void test (int x, int n, int b) {
        if (b == 0) {
            assume n >= 0;
            assert inv(0, n) == 1;
        } else if (b == 1) {
            assume inv(x, n) == 1;
            assume x < n;
            assert inv(x + 1, n) == 1;
        } else {
            assume inv(x, n) == 1;
            assume x >= n;
            assert x == n;
        }
    }
}
