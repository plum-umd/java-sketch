class ABC {
    String name;

    public ABC (String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }
}

class XYZ {
    StringBuffer buf;

    public XYZ (String name) {
        this.buf = new StringBuffer(name);
    }

    public void setCharAt(int i, char c) {
        this.buf.setCharAt(i, c);
    }

    public String getName() {
        return this.buf.toString();
    }
}

class Test {
    harness static void test_string () {
        String msg = "Hello, World";
        ABC a = new ABC(msg);
        assert msg.equals(a.getName());
    }

    harness static void test_buf () {
        String msg = "Hello, World";
        XYZ x = new XYZ(msg);
        x.setCharAt(0, 'h');
        assert ! msg.equals(x.getName());
    }
}
