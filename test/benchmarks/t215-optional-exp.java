class ABC {
    public static int cnt = 0;

    static void inc() { cnt = cnt + 1; }

    // suppose we don't know how many times to call a certain method
    static void foo() {
        if (??) { inc(); }
        if (??) { inc(); }
        if (??) { inc(); }
    }

    harness static void test() {
        foo();
        // either block will be chosen
        assert cnt == 1;
    }
}
