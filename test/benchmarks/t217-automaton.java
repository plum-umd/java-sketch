/*
interface Token{
    public int getId();
}
*/

generator class Automaton {
    private int state = 0;
/*
    public void transition(Token t) {
        int id = t.getId();
*/
    public void transition(int id) {
        minrepeat {
            if (state == ?? && id == ??) { state = ??; return; }
        }
    }

    public void transitions(Iterator it) {
        while (it.hasNext()) {
            transition(it.next());
        }
    }

    public boolean accept() {
        return state <= ??;
    }
}

class CADsR extends Automaton {
    public CADsR() { }

    class CharIterator implements Iterator {
        private final String str;
        private int pos;

        public CharIterator(String str) {
            this.str = str;
            this.pos = 0;
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
        transitions(cit);
        return accept();
    }
}

class DBConnection {

    class Monitor extends Automaton {
        final static int OPEN = 1;
/*
        final static Token OPEN = new Token() {
            public int getId() { return 1; }
        };
*/
        final static int CLOSE = 2;
/*
        final static Token CLOSE = new Token() {
            public int getId() { return 2; }
        };
*/
        public Monitor() { }
    }

    Monitor m;
    public DBConnection() {
        m = new Monitor();
    }

    public boolean isErroneous() {
        return ! m.accept();
    }

    public void open() {
        m.transition(Monitor.OPEN);
    }

    public void close() {
        m.transition(Monitor.CLOSE);
    }
}

class Test {

    // Lisp-style identifier: c(a|d)+r
    harness static void test_CADsR() {
        CADsR a = new CADsR();
        // length 1
        assert ! a.accept("a");
        assert ! a.accept("c");
        assert ! a.accept("d");
        assert ! a.accept("r");

        // length 2
        assert ! a.accept("aa");
        assert ! a.accept("ac");
        assert ! a.accept("ad");
        assert ! a.accept("ar");
        assert ! a.accept("ca");
        assert ! a.accept("cc");
        assert ! a.accept("cd");
        assert ! a.accept("cr");
        assert ! a.accept("da");
        assert ! a.accept("dc");
        assert ! a.accept("dd");
        assert ! a.accept("dr");
        assert ! a.accept("ra");
        assert ! a.accept("rc");
        assert ! a.accept("rd");
        assert ! a.accept("rr");
        assert ! a.accept("cr");

        // length 3
        assert ! a.accept("caa");
        assert ! a.accept("cad");
        assert a.accept("car");
        assert ! a.accept("cda");
        assert ! a.accept("cdd");
        assert a.accept("cdr");

        // length 4
/*
        assert ! a.accept("caaa");
        assert ! a.accept("caad");
        assert a.accept("caar");
        assert ! a.accept("cada");
        assert ! a.accept("cadd");
        assert a.accept("cadr");
        assert ! a.accept("cdaa");
        assert ! a.accept("cdad");
        assert a.accept("cdar");
        assert ! a.accept("cdda");
        assert ! a.accept("cddd");
        assert a.accept("cddr");
*/
    }

    harness static void test_DBConnection_good() {
        DBConnection conn = new DBConnection();
        conn.open();
        assert ! conn.isErroneous();
        conn.close();
        assert ! conn.isErroneous();
    }

    // bad: closing more than once
    harness static void test_DBConnection_bad1() {
        DBConnection conn = new DBConnection();
        conn.open();
        conn.close();
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

