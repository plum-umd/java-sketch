@axiomClass
class TreeSet {

    @adt
    boolean add(Object e);
    
    @adt
    Object clear();

    @adt
    boolean contains(Object e);

    @adt
    @pure
    int size();

    axiom Object size(Object TreeSet()) {
	return 0;
    }

    axiom Object size(Object add!(TreeSet s, Object e)) {
	boolean b = contains(s, e);
	if (b) {
	    return size(s);
	} else {
	    return size(s)+1;
	}
	// return contains(s, e) ? size(s) : size(s)+1;
    }

    axiom Object size(Object clear!(TreeSet s)) {
	return 0;
    }
    
    axiom Object add(Object clear!(TreeSet s), Object e) {
    	return true;
    }
    
    axiom Object add(Object TreeSet(), Object e) {
    	return true;
    }

    axiom Object add(Object add!(TreeSet s, Object e1), Object e2) {
    	return e2.equals(e1) ? false : add(s, e2);
    }

    axiom Object contains(Object add!(TreeSet s, Object e1), Object e2) {
    	return e1.equals(e2) ? true : contains(s, e2);
    }

    axiom Object contains(Object TreeSet(), Object e) {
	return false;
    }

    axiom Object contains(Object clear!(TreeSet s), Object e) {
    	return false;
    }

}
