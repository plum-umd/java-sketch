import java.util.Iterator;


class Token{
    int id; 
    public int getId() { return this.id; }
}

class Automaton {
// generator class Automaton {
    int state;
    public Automaton() {
        state = 0;
    }

    static int num_state = 0;
     static void min_num_state() {
        // minimize(num_state);
    }


    public void transition(Token t) {
        int id = t.getId();
    }

    public void transition(int id) {
        assert 0 <= state && state < num_state;
        // minrepeat {
        //     if (state == 0 && id == 0) { state = 0; return; }
        // }
    }

    public void transition(Iterator it) {
        while (it.hasNext()) {
            transition((Token)it.next());
        }
    }

    public boolean accept() {
        return state <= 0;
    }
}

class CADsR extends Automaton {
    public CADsR() {
        super();
    }

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

        public Integer next() {
            Character c = str.charAt(pos);
            pos = pos + 1;
            return (Integer)c;
        }

        public void remove() {
            //throw new UnsupportedOperationException();
        }
    }

    public boolean accept(String str) {
        state = 0; // reset
        CharIterator cit = new CharIterator(str);
        transition(cit);
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
        public Monitor() {
            super();
        }
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

// Lisp-style identifier: c(a|d)+r
class TestCADsR {
    harness void mn() {
    	example_0();
    }
    // length 0
     static void example_0() {
        CADsR a = new CADsR();
        assert ! a.accept();
    }

    // length 1
     static void example_1() {
        CADsR a = new CADsR();
        assert ! a.accept("a");
        assert ! a.accept("c");
        assert ! a.accept("d");
        assert ! a.accept("r");
    }

    // length 2
     static void example_2() {
        CADsR a = new CADsR();
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
    }

    // length 3
     static void example_3() {
        CADsR a = new CADsR();

        // length 3
        //assert ! a.accept("caa");
        //assert ! a.accept("cad");
        assert a.accept("car");
        //assert ! a.accept("cda");
        //assert ! a.accept("cdd");
        assert a.accept("cdr");
    }

    // length 4
     static void example_4() {
        CADsR a = new CADsR();

        //assert ! a.accept("caaa");
        //assert ! a.accept("caad");
        assert a.accept("caar");
        //assert ! a.accept("cada");
        //assert ! a.accept("cadd");
        assert a.accept("cadr");
        //assert ! a.accept("cdaa");
        //assert ! a.accept("cdad");
        assert a.accept("cdar");
        //assert ! a.accept("cdda");
        //assert ! a.accept("cddd");
        assert a.accept("cddr");
    }

}

class TestDBConnection {
     static void scenario_good() {
        DBConnection conn = new DBConnection();
        assert ! conn.isErroneous();
        conn.open();
        assert ! conn.isErroneous();
        conn.close();
        assert ! conn.isErroneous();
    }

    // bad: opening more than once
     static void scenario_bad1() {
        DBConnection conn = new DBConnection();
        conn.open();
        conn.open();
        assert conn.isErroneous();
    }

    // bad: closing more than once
     static void scenario_bad2() {
        DBConnection conn = new DBConnection();
        conn.open();
        conn.close();
        conn.close();
        assert conn.isErroneous();
    }

}

