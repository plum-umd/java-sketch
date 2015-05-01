class A {
}

class B extends A {
    public int[] x;
    public A a;
}

class C extends A {
    public int x;
}

class Testb626 {

    static int h = ??;

    harness static void main (int x) {
        B b = new B();
        C c = new C();
        c.x = x;

        if (h) {
            b.a = b;
        } else {
            b.a = c;
        }

        C cc = (C) b.a;
        assert cc.x == x;
    }
}
