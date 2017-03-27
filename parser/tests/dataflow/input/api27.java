class Switch {
    void m() {
	int x = 0;
	int y = x + 1;
	switch (x) {
	case 1:
	    x = 0;
	case 2:
	    x = 1;
	}
    }
}
