class ThisGenerator {
    int x;
    harness void mn() {
	this.x = 0;
	if ({|this.x|} == 1) assert true;
    }
}
