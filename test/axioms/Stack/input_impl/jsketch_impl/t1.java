class t1 {
    harness void m() {
	Stack s = new Stack<Object>();
	Object o1 = new Object();
	Object o2 = new Object();

	s.push(o1);
	s.push(o2);
	Object poppsh12 = s.pop();

	assert poppsh12.equals(o2);
    }
}
