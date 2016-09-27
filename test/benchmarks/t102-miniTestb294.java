class F extends A {
    int x;
    int getX() {
        return this.x;
    }

    void setX(int v) {
        this.x = v;
    }
}

class Testb294 {
    harness static void test(int v) {
        F t = new F();
        t.setX(v);
        assert v == t.getX();
    }
}
