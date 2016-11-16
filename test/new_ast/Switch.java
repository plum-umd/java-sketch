class Switch {
    harness static void main() {
	int x = 1;
	switch (x) {
    	case 0:
	    x = 2;
	case 1:
	    x = 3;
	case 2:
	    x = 4;
	}
	assert x == 3;
    }
}
