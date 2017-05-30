class GenAsArg {
    harness void mn(int x, int y) {
	assert same({|x,y|}) == x;
    }
    int same(int x) {
	return x;
    }
    
}
