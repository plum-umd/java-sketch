class ArrayDeque {
    harness void mn() { }
}

@axiomClass
class AxArrayDeque {

    @adt
    @pure
    int size();

    @adt
    Object removeFirst();

    @adt
    Object removeLast();

    @adt
    void addFirst(Object e);

    @adt
    void addLast(Object e);
    
    @adt
    Object peekFirst();

    @adt
    Object peekLast();

    @adt
    @pure
    boolean isEmpty();

    axiom Object removeFirst(Object addFirst!(AxArrayDeque d, Object e)) {
	return e;
    }

    axiom Object removeFirst(Object addLast!(AxArrayDeque d, Object e)) {
	return size(d) == 0 ? e : removeFirst(d.self);
    }

    axiom Object removeLast(Object addLast!(AxArrayDeque d, Object e)) {
	return e;
    }

    axiom Object removeLast(Object addFirst!(AxArrayDeque d, Object e)) {
	return size(d) == 0 ? e : removeLast(d.self);
    }

    axiom Object peekFirst(Object addFirst!(AxArrayDeque d, Object e)) {
	return e;
    }

    axiom Object peekFirst(Object addLast!(AxArrayDeque d, Object e)) {
	return size(d) == 0 ? e : peekFirst(d.self);
    }

    axiom Object peekLast(Object addLast!(AxArrayDeque d, Object e)) {
	return e;
    }

    axiom Object peekLast(Object addFirst!(AxArrayDeque d, Object e)) {
	return size(d) == 0 ? e : peekLast(d.self);
    }

    axiom Object size(Object AxArrayDeque()) {
	return 0;
    }

    axiom Object size(Object addFirst!(AxArrayDeque d, Object e)) {
	return 1 + size(d.self);
    }

    // Doesn't work, not sure why
    // axiom Object isEmpty(AxArrayDeque d) {
    // 	return size(d) == 0 ? true : false;
    // }
}
