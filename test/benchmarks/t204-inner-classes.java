class Outer1 {
    class Inner {
        final static int C1 = ??;
        final static int C2 = ??;
    }

    harness static void assign () {
        assert Inner.C1 != Inner.C2; // now distinct integers will be assigned
    }
}

class Outer2 extends Outer1 {
    class InnerExt extends Outer1.Inner {
    }

    static int h1 = ??;
    static int h2 = ??;

    harness static void test () {
        // test whether we can access to base inner class's constants
        assert h1 == InnerExt.C1;
        assert h2 == InnerExt.C2;
        // and double-check that they are indeed different
        assert h1 != h2;
    }
}
