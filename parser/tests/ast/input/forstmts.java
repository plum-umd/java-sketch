class ForStmt {
    void m() {
	int x = 0, y = 0;
	for (x=0; x>10; x++) {
	    y = y + 1;
	}
	for (x=0, y=0; x>10; x = x + 1, y = y - 1) {
	    int x=10;
	    x = x + y;
	}
	x++;
    }
}
