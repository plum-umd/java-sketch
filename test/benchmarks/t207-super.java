class Base {
    public int x;

    public Base (int x) {
        this.x = x;
    }

    public void foo() {
        this.x = this.x + this.x;
    }
}

class Ext extends Base {
    public Ext (int x) {
        super(x);
        this.x = this.x + 1;
    }

    @Override
    public void foo() {
        super.foo();
        super.foo();
    }
}

class Test {
    harness static void test (int x) {
        Base b = new Base(x);
        assert b.x == x;
        b.foo();
        assert b.x == x * 2;

        Ext e = new Ext(x);
        assert e.x == x + 1;
        e.foo();
        assert e.x == x * 4 + 4; // (x + 1) * 2 * 2
    }
}
