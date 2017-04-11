class t4 {
    harness void m() {
	Stack s = new Stack<Object>();
	Object o1 = new Object();
	Object o2 = new Object();

	s.push(o1);
	s.push(o2);
	s.pop();
	Object poppoppsh12 = s.pop();

	assert poppoppsh12.equals(o1);
    }
}
