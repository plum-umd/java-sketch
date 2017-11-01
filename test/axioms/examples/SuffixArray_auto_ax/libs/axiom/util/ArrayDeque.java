@axiomClass
class ArrayDeque {
    @adt
    @pure
    Object peekFirst();

    @adt
    @pure
    Object peekFirst_help(int i, int j);
    
    @adt
    @pure
    boolean isEmpty();

    @adt
    Object removeFirst();

    @adt
    @pure
    Object peekLast();

    @adt
    @pure
    Object peekLast_help(int i, int j);
    
    @adt
    Object removeLast();

    @adt
    void addLast(Object e);

    @adt
    @pure
    int size();

    axiom Object size(Object ArrayDeque()) {
	return 0;
    }
    
    axiom Object size(Object addLast!(ArrayDeque d, Object e)) {
    	return size(d)+1;
    }

    axiom Object size(Object removeFirst!(ArrayDeque d, Object e)) {
    	return size(d)==0 ? 0 : size(d)-1;
    }

    axiom Object size(Object removeLast!(ArrayDeque d, Object e)) {
    	return size(d)==0 ? 0 : size(d)-1;
    }

    axiom Object isEmpty(ArrayDeque d) {
    	return size(d)==0;
    }

    axiom Object peekLast(Object ArrayDeque()) {
	return null;
    }
    
    axiom Object peekLast(Object addLast!(ArrayDeque d, Object e)) {
    	return e;
    }

    axiom Object peekLast(Object removeLast!(ArrayDeque d)) {
	return peekLast_help(d, 0, 1);
    }

    axiom Object peekLast_help(Object removeLast!(ArrayDeque d), int i, int j) {
	return peekLast_help(d,i,j+1);
    }

    axiom Object peekLast(Object removeFirst!(ArrayDeque d)) {
	return peekLast_help(d, 1, 0);
    }

    axiom Object peekLast_help(Object removeFirst!(ArrayDeque d), int i, int j) {
	return peekLast_help(d, i+1, j);
    }
    
    axiom Object peekLast_help(Object addLast!(ArrayDeque d, Object e), int i, int j) {
	if (j > 0) {
	    return peekLast_help(d, i, j-1);
	} else if (i > 0) {
	    return size(d) == 0 ? null : e;
	} else {
	    return e;
	}
    }

    axiom Object peekFirst(Object ArrayDeque()) {
	return null;
    }
    
    axiom Object peekFirst(Object addLast!(ArrayDeque d, Object e)) {
	return size(d)==0 ? e : peekFirst(d);
    }

    axiom Object peekFirst(Object removeFirst!(ArrayDeque d)) {
	return peekFirst_help(d, 1, 0);
    }

    axiom Object peekFirst(Object removeLast!(ArrayDeque d)) {
	return peekFirst_help(d, 0, 1);
    }

    axiom Object peekFirst_help(Object removeFirst!(ArrayDeque d), int i, int j) {
	return peekFirst_help(d, i+1, j);
    }

    axiom Object peekFirst_help(Object removeLast!(ArrayDeque d), int i, int j) {
	return peekFirst_help(d, i, j+1);
    }

    axiom Object peekFirst_help(Object addLast!(ArrayDeque d, Object e), int i, int j) {
	if (size(d) == i) {
	    if (j > 0) {
		return null;
	    }
	    return e;
	} else {
	    return peekFirst_help(d, i, j-1);
	}
    }

    axiom Object removeLast(ArrayDeque d) {
	return peekLast(d);
    }

    axiom Object removeFirst(ArrayDeque d) {
	return peekFirst(d);
    }
}
