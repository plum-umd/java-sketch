interface Constants {
    final static int C1 = ??;
    final static int C2 = ??;
    final static int C3 = ??;
}

class ABC implements Constants {
    int bogus;
}

class Test {
    harness static void test () {
        assert ABC.C1 != ABC.C2;
        assert ABC.C1 != ABC.C3;
        assert ABC.C2 != ABC.C3;
    }
}
