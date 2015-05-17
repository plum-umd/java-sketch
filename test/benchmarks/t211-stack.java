class Plate {
    static int count = 0;
    static int nonce () {
        count = count + 1;
        return count;
    }

    public int hash;

    public Plate() {
        hash = Plate.nonce();
    }
}

class PlateStack {
    Stack<Plate> ps;

    public PlateStack() {
        ps = new Stack<Plate>();
    }

    public Plate peek() {
        return ps.peek();
    }

    public void push(Plate p) {
        ps.push(p);
    }

    public Plate pop() {
        return ps.pop();
    }
}

class Test {
    harness static void test () {
        Plate top;
        PlateStack ps = new PlateStack();
        Plate p = new Plate();
        assert p.hash == 1;
        ps.push(p);
        top = ps.peek();
        assert top.hash == 1;
        p = new Plate();
        assert p.hash == 2;
        ps.push(p);
        top = ps.peek();
        assert top.hash == 2;
        p = new Plate();
        assert p.hash == 3;
        ps.push(p);
        top = ps.peek();
        assert top.hash == 3;

        p = ps.pop();
        assert p.hash == 3;
        top = ps.peek();
        assert top.hash == 2;
        p = ps.pop();
        assert p.hash == 2;
        top = ps.peek();
        assert top.hash == 1;
        p = ps.pop();
        assert p.hash == 1;
    }
}
