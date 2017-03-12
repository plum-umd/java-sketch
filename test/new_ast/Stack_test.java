class Stack_test {
    harness void m() {
	Stack s = new Stack<String>();
	String s1 = "One";
	String s2 = "Two";
	String s3 = "Three";
	String check, p1, p2, p3;

	// empty, push, pop, search, peek
	assert s.empty();
	
	check = s.push(s1);
	p1 = s.pop();

	assert check.equals(s1);
	assert p1.equals(s1);

	s.push(s2);
	s.push(s3);
	p3 = s.pop();
	p2 = s.pop();

	assert p3.equals(s3);
	assert p2.equals(s2);

	s.push(s3);
	s.push(s2);
	s.push(s1);

	check = s.peek();

	assert !s.empty();
	assert check.equals(s1);
	assert s.search(s1) == 2;
	assert s.search(s2) == 1;
	assert s.search(s3) == 0;

	p1 = s.pop();
	p2 = s.pop();
	p3 = s.pop();

	assert s.empty();
	assert p1.equals(s1);
	assert p2.equals(s2);
	assert p3.equals(s3);
    }
}
