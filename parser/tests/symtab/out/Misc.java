class C {
    int f0;
    static int f1;
    int m0(int p0, String p1) {
        int a = (1 + 2 + 3);
        String b;
        b = p1;
        return a;
    }
    int m1(int p0, int p1, int f0) {
        this.f0 = f0;
        if (p0 != p1) {
            p0 = p1;
            return p0;
        }
        else if (p0 < p1) {
            if (p0 == 0) {
                return 0;
            }
        }
        else {
            int p2;
            p2 = p1;
            return p2;
        }
        return 0;
    }
    static void m2() {
        assert 0 == 0 : "This is a string.";
        int x = 0;
        int a, b, c = (1 + 2);
    }
}
class A {
    int m0_A() {
        return m1_A();
    }
    int m1_A() {
        C c = new C();
        int x = 1;
        c.f0 = 0;
        c.m1(0, x, 1);
        C.f1 = 0;
        C.m2();
        return 1 + 2;
    }
}

