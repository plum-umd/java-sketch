class S {
    static int static_fld;
    int non_static_fld;
    public static void static_mtd() {
    	int sta = static_fld;
	assert sta == 1;
    }

    public void non_static_mtd() {
    	int sta = static_fld;
    	int non = non_static_fld;
	assert sta == 1;
	assert non == 2;
    }
}

class Static {
    harness void statics() {
	S s = new S();
	S.static_fld = 1;
	s.non_static_fld = 2;

	int sfld = S.static_fld;
	int nfld = s.non_static_fld;

	assert sfld == 1;
	assert nfld == 2;
	
	s.static_mtd();
	s.non_static_mtd();
    }
}
