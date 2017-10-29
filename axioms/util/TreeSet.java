@axiomClass
class TreeSet {

    @adt
    boolean add(Object e);
    
    @adt
    Object clear();

    @adt
    boolean contains(Object e);

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
