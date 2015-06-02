/*
interface Token{
    public int getId();
}
*/

generator class Automaton {
    int state = 0;
/*
    public void transition(Token t) {
        int id = t.getId();
*/
    public void transition(int id) {
        minrepeat {
            if (state == ?? && id == ??) { state = ??; return; }
        }
    }

    public boolean accept(Iterator it) {
        while (it.hasNext()) {
            transition(it.next());
        }
        return state == ??;
    }

    public boolean isErroneous() {
        return state == ??;
    }
}

class CADsR extends Automaton {
    public CADsR() { }

    class CharIterator implements Iterator {
        private final String str;
        private int pos = 0;

        public CharIterator(String str) {
            this.str = str;
        }

        public boolean hasNext() {
            return pos < str.length();
        }

        public int next() {
            Character c = str.charAt(pos);
            pos = pos + 1;
            return (int)c;
        }

        public void remove() {
            //throw new UnsupportedOperationException();
        }
    }

    public boolean accept(String str) {
        CharIterator cit = new CharIterator(str);
        return accept(cit);
    }
}

class DBConnection {

    class Monitor extends Automaton {
        final static int OPEN = 1;
        final static int CLOSE = 2;
        public Monitor() { }
    }

    Monitor m;
    public DBConnection() {
        m = new Monitor();
    }

    public boolean isErroneous() {
        return m.isErroneous();
    }

    public void open() {
/*
        Token t = new Token() {
            public int getId() { return Monitor.OPEN; }
        };
        m.transition(t);
*/
        m.transition(Monitor.OPEN);
    }

    public void close() {
/*
        Token t = new Token() {
            public int getId() { return Monitor.CLOSE; }
        };
        m.transition(t);
*/
        m.transition(Monitor.CLOSE);
    }
}

class Test {
    // Lisp-style identifier: c(a|d)+r
    harness static void test_CADsR() {
        CADsR a = new CADsR();
        assert ! a.accept("cr");
        assert a.accept("car");
        assert a.accept("cdr");
        assert ! a.accept("cad");
        assert ! a.accept("cda");
        assert a.accept("cadr");
        assert ! a.accept("cady");
    }

    harness static void test_DBConnection_good() {
        DBConnection conn = new DBConnection();
        conn.open();
        assert ! conn.isErroneous();
        conn.close();
        assert ! conn.isErroneous();
    }

    // bad: close without opening
    harness static void test_DBConnection_bad1() {
        DBConnection conn = new DBConnection();
        conn.close();
        assert conn.isErroneous();
    }

    // bad: opening more than once
    harness static void test_DBConnection_bad2() {
        DBConnection conn = new DBConnection();
        conn.open();
        conn.open();
        assert conn.isErroneous();
    }

}

