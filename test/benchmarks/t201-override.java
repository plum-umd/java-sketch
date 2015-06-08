interface ICar {
    public int kind();
}

abstract class ACar implements ICar {
    public int kind() {
        return 0;
    }
}

class Sedan extends ACar {
    public Sedan() { }
    @Override
    public int kind() {
        return 1;
    }
}

class SUV extends ACar {
    public SUV() { }
    @Override
    public int kind() {
        return 2;
    }
}

class Test {
    harness static void test() {
        ICar x = new Sedan();
        ICar y = new SUV();
        assert x.kind() != y.kind();
        assert x.kind() == 1;
        assert y.kind() == 2;
    }
}
