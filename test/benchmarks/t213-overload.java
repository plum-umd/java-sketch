class Flipper {
    public static boolean flip (boolean x) {
        return !x;
    }

    public static int flip (int x) {
        if (x == 0) return h;
        else return 0;
    }

    static int h = ??;

    harness static void assign_h () {
        assert h != 0;
    }
}

class Test {
    harness static void test () {
        assert Flipper.flip(false);
        assert ! Flipper.flip(true);
        assert 0 == Flipper.flip(1);
        assert 0 != Flipper.flip(0);
    }
}
