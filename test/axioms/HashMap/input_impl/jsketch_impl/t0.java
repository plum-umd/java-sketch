class t0 {
    harness void m() {
	Stack s = new Stack<Object>();
	Object o1 = new Object();

	s.push(o1);
	Object poppsh1 = s.pop();

	assert poppsh1.equals(o1);
    }
}
