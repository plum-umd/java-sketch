class t5 {
    harness void m() {
	Stack s = new Stack<Object>();
	Object o1 = new Object();
	Object o2 = new Object();
	Object o3 = new Object();
	Object o4 = new Object();
	Object o5 = new Object();

	s.push(o1);
	s.pop();
	s.push(o2);
	s.pop();
	s.push(o3);
	s.pop();
	s.push(o4);
	s.pop();
	s.push(o5);
	Object poppsh5 = s.pop();

	assert poppsh5.equals(o5);
    }
}
