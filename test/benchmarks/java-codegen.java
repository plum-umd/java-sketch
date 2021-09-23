@JavaCodeGen
class SimpleMath {
    static int zero = 0;
    static int mult2(int x) {
        return multi_by_factor(x);
    }
    generator static int multi_by_factor(int x) {
        return x * ??;
    }
}

class Test {
    harness static void test() {
        assert SimpleMath.mult2(3) == 6;
    }
}