class B {
    void b() {
	int x = 0;
	switch (x) {
	case 1:
	    x = 2;
	case 2:
	    x = 3;
	case 3:
	    x = x + 4;
	}
    }
}
