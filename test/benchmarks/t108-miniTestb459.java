class Testb459 {
    harness static void main(int x) {
        int t = x;
        minrepeat {
            x = x + 1;
        }
        assert x > t + 2; // the above will be unrolled more than twice
    }
}
