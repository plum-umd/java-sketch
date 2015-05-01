interface ICar {
    public int kind();
}

class ACar implements ICar {
    public int kind() { return 0; }
}

class Sedan extends ACar {
}

class SUV extends ACar {
    @Override
    public int kind() { return 1; }
}

class Test {
    harness static void test() {
        Sedan x = new Sedan();
        SUV y = new SUV();
        assert x.kind() != y.kind();
    }
}
