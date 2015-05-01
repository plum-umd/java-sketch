class ABC {
    static int foo() {
        // no return
    }

    harness static void test (int x) {
        assert x == foo();
    }
}
