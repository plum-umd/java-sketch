class BoolArg {
    boolean isTrue(boolean condition) { return condition; }
    harness void mn() {
	assert isTrue(2 > 1);
    }

}
