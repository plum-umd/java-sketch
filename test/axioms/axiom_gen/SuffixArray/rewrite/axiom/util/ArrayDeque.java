@rewriteClass
class ArrayDeque {
    @alg
    @pure
    Object peekFirst();

    @alg
    @pure
    Object peekFirstHelp(int i, int j);
    
    @alg
    @pure
    boolean isEmpty();

    @alg
    Object removeFirst();

    @alg
    @pure
    Object peekLast();

    @alg
    @pure
    Object peekLastHelp(int i, int j);
    
    @alg
    Object removeLast();

    @alg
    void addLast(Object e);

    @alg
    @pure
    int size();

    rewrite Object size(Object ArrayDeque()) {
	return 0;
    }
    
    rewrite Object size(Object addLast!(ArrayDeque d, Object e)) {
    	return size(d)+1;
    }

    rewrite Object size(Object removeFirst!(ArrayDeque d, Object e)) {
    	return size(d)==0 ? 0 : size(d)-1;
    }

    rewrite Object size(Object removeLast!(ArrayDeque d, Object e)) {
    	return size(d)==0 ? 0 : size(d)-1;
    }

    // rewrite Object isEmpty(ArrayDeque d) {
    // 	return size(d)==0;
    // }

    rewrite Object peekLast(Object ArrayDeque()) {
	return null;
    }
    
    rewrite Object peekLast(Object addLast!(ArrayDeque d, Object e)) {
    	return e;
    }

    rewrite Object peekLast(Object removeLast!(ArrayDeque d)) {
	return peekLastHelp(d, 0, 1);
    }

    rewrite Object peekLastHelp(Object removeLast!(ArrayDeque d), int i, int j) {
	return peekLastHelp(d,i,j+1);
    }

    rewrite Object peekLast(Object removeFirst!(ArrayDeque d)) {
	return peekLastHelp(d, 1, 0);
    }

    rewrite Object peekLastHelp(Object removeFirst!(ArrayDeque d), int i, int j) {
	return peekLastHelp(d, i+1, j);
    }
    
    rewrite Object peekLastHelp(Object addLast!(ArrayDeque d, Object e), int i, int j) {
	if (j > 0) {
	    return peekLastHelp(d, i, j-1);
	} else if (i > 0) {
	    return size(d) == 0 ? null : e;
	} else {
	    return e;
	}
    }

    rewrite Object peekFirst(Object ArrayDeque()) {
	return null;
    }
    
    rewrite Object peekFirst(Object addLast!(ArrayDeque d, Object e)) {
	return size(d)==0 ? e : peekFirst(d);
    }

    rewrite Object peekFirst(Object removeFirst!(ArrayDeque d)) {
	return peekFirstHelp(d, 1, 0);
    }

    rewrite Object peekFirst(Object removeLast!(ArrayDeque d)) {
	return peekFirstHelp(d, 0, 1);
    }

    rewrite Object peekFirstHelp(Object removeFirst!(ArrayDeque d), int i, int j) {
	return peekFirstHelp(d, i+1, j);
    }

    rewrite Object peekFirstHelp(Object removeLast!(ArrayDeque d), int i, int j) {
	return peekFirstHelp(d, i, j+1);
    }

    rewrite Object peekFirstHelp(Object addLast!(ArrayDeque d, Object e), int i, int j) {
	if (size(d) == i) {
	    if (j > 0) {
		return null;
	    }
	    return e;
	} else {
	    return peekFirstHelp(d, i, j-1);
	}
    }

    // rewrite Object removeLast(ArrayDeque d) {
    // 	return peekLast(d);
    // }

    // rewrite Object removeFirst(ArrayDeque d) {
    // 	return peekFirst(d);
    // }
}
