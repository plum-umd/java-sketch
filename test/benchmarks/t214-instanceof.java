class Expression {
    public Expression() {
    }
}

class IDExp extends Expression {
    protected String id;

    public IDExp(String id) {
        this.id = id;
    }
}

class BinaryExp extends Expression {
    protected Expression le;
    protected Expression re;

    public BinaryExp(Expression le, Expression re) {
        this.le = le;
        this.re = re;
    }
}

class CallExp extends Expression {
    protected Expression e;
    //protected List<Expression> args;

    //public CallExp(Expression e, List<Expression> args) {
    public CallExp(Expression e) {
        this.e = e;
        /*
        if (args != null) {
			this.args = new List<Expression>();
			for (Expression arg : args) {
				this.args.add(arg);
			}
        }
        */
    }
}

class CallFinder {
    public static boolean hasCall(Expression e) {
        if (e instanceof IDExp) {
            return false;
        } else if (e instanceof BinaryExp) {
            BinaryExp be = (BinaryExp)e;
            boolean h_le = CallFinder.hasCall(be.le);
            if (h_le) return true;
            boolean h_re = CallFinder.hasCall(be.re);
            return h_re;
        } else if (e instanceof CallExp) {
            return true;
        } else {
            return false;
        }
    }
}

class Test {
    harness static void test () {
        Expression e1 = new IDExp("foo");
        Expression e2 = new CallExp(e1); // new CallExp(e1, null);
        Expression e3 = new BinaryExp(e1, e2);
        assert ! CallFinder.hasCall(e1);
        assert CallFinder.hasCall(e2);
        assert CallFinder.hasCall(e3);
    }
}
