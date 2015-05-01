class ABC {
    int x;

    public ABC() {
        this.x = 0;
    }
}

class Test {
    harness static void test_obj () {
		Object a = new Object();
		Object b = new Object();
        assert a == a;
        assert b == b;
        assert a != b;
    }

    harness static void test_abc () {
        ABC a = new ABC();
        ABC b = new ABC();
        assert a == a;
        assert b == b;
        assert a != b;
    }
}
