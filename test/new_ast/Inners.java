class Out {
    int f_out;
    class In {
	int f_in;
	void inner_m0(int x) {
	    f_in = x + 1;
	    f_out = x + 2;
	}
    }
    void outer_m0() {
	In in = new In();
	in.inner_m0(2);
	assert in.f_in == 3;
	assert in.f_out == 4;
    }
}

class Inners {
    harness void Inners() {
	Out o = new Out();
	o.outer_m0();
	o.inner_m0(0);
	assert o.f_in == 1;
	assert o.f_out == 2;
    }
}
