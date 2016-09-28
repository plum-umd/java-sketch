class SimpleMath {
    static int mult2(int x) {
	return 0;
        // return ?? * {| x , 0 |};
    }
}

class TestSimpleMath {
    harness static void test() {
        assert SimpleMath.mult2(3) == 6;
    }
}
