class t3 {
    harness void m() {
	Stack s = new Stack<Object>();
	Object o1 = new Object();
	Object o2 = new Object();

	s.push(o1);
	s.pop();
	s.push(o2);
	Object poppshpoppsh12 = s.pop();

	assert poppshpoppsh12.equals(o2);
    }
}
