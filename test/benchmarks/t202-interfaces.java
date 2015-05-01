interface Ix {
    int foo();
}

interface Iy extends Ix {
    int bar();
}

class Ax implements Ix {
    int foo() {
        return 0;
    }
}

class Ay extends Ax implements Iy {
    int bar() {
        return 1;
    }
}

class Test {
    harness static void test () {
        Ay y = new Ay();
        assert y.foo() != y.bar();
    }
}
