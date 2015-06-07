class SimpleMath {
    static int mult2(int x) {
        return ?? * {| x , 0 |};
    }
}

class TestSimpleMath {
    harness static void test() {
        assert SimpleMath.mult2(3) == 6;
    }
}
