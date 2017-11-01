@axiomClass
class HashSet {

    @adt
    boolean add(Object e2);

    @adt
    boolean remove(Object e2);

    @adt
    @pure
    int size();

    axiom Object add(Object HashSet(), Object e) {
    	return true;
    }

    axiom Object add(Object add!(HashSet h, Object e1), Object e2) {
    	return e2.equals(e1) ? false : add(h, e2);
    }

    axiom Object remove(Object HashSet(), Object e) {
    	return false;
    }

    axiom Object remove(Object add!(HashSet h, Object e1), Object e2) {
    	return e2.equals(e1) ? true : remove(h, e2);
    }

    axiom Object remove(Object remove!(HashSet h, Object e1), Object e2) {
    	return e2.equals(e1) ? false : remove(h, e2);
    }

    axiom Object size(Object HashSet()) {
    	return 0;
    }
    
    axiom Object size(Object add!(HashSet h, Object e1)) {
    	return size(h) + 1;
    }

    axiom Object size(Object remove!(HashSet h, Object e1)) {
	return remove(h, e1) ? size(h)-1 : size(h);
    }
}
