class t6 {
    harness void m() {
	Stack s = new Stack<Object>();
	Object o1 = new Object();
	Object o2 = new Object();
	Object o3 = new Object();
	Object o4 = new Object();
	Object o5 = new Object();

	s.push(o1);
	s.push(o2);
	s.push(o3);
	s.push(o4);
	s.push(o5);
	s.pop();
	s.pop();
	s.pop();
	s.pop();
	Object poppsh1 = s.pop();

	assert poppsh1.equals(o1);
    }
}
