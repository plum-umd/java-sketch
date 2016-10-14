class S {
    static int static_fld;
    int non_static_fld;
    public static void static_mtd() {
    	int sta = static_fld;
    }

    public void non_static_mtd() {
    	int non = non_static_fld;
    	int sta = static_fld;
    }
}

class Static {
    harness void statics() {
	S s = new S();

	int sfld = S.static_fld;
	int nfld = s.non_static_fld;

	s.static_mtd();
	s.non_static_mtd();
    }
}
