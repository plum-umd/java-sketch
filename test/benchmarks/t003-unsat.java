class UNSAT {
    static int hole = ??;

    static int foo(int x) {
        return x + 1;
    }

    harness static void test() {
        assert hole == UNSAT.foo(hole);
    }
}
