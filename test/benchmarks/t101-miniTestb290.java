class Testb290 {
    harness void test (int a, int b) {
        int x = Foo.foo(a) + Boo_Moo.moo(b) + Boo_Moo.boo(a, b);
        assert x == (a + b + a);
    }
}

class Foo {
    public static int foo (int x) {
        return x;
    }
}

class Boo_Moo {
    public static int moo (int y) {
        return y;
    }

    public static int boo (int x, int y) {
       return ?? * x + ?? * y;
    }
}
