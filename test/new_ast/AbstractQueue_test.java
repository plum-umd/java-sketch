class AbstractQueue_test {
    harness void m() {
	AbstractQueue<String> q = new AbstractQueue<String>();
	String s1 = "One";
	String s2 = "Two";
	String s3 = "Three";
	String e, r1, r2, r3;

	q.add(s1);
	q.add(s2);
	q.add(s3);

	e = q.element();
	
	assert e.equals(s1);

	r1 = q.remove();
	e = q.element();
	r2 = q.remove();
	r3 = q.remove();

	assert r1.equals(s1);
	assert e.equals(s2);
	assert r2.equals(s2);
	assert r3.equals(s3);

	q.add(s3);
	q.add(s2);
	q.add(s1);

	e = q.element();
	
	assert e.equals(s3);

	q.clear();

	e = q.element();
	r1 = q.remove();
	r2 = q.remove();
	r3 = q.remove();

	assert e == null;
	assert r1 == null;
	assert r2 == null;
	assert r3 == null;
    }
}
