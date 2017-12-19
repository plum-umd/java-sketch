@axiomClass
class TreeSet {

    @adt
    boolean add(Object e);
    
    @adt
    Object clear();

    @adt
    @pure
    boolean contains(Object e);

    @adt
    @pure
    int size();

    @adt
    @pure
    Object last();
    
    @adt
    boolean remove(Object e);

    axiom Object size(Object TreeSet()) {
	return 0;
    }

    axiom Object size(Object add!(TreeSet s, Object e)) {
	return contains(s, e) ? size(s) : size(s)+1;
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
    
    axiom Object last(Object add!(Treeset s, Object e1))
    {
	return last(s).compareTo(e1) > 0 ? last(s) : e1;
    }

    axiom Object size(Object remove!(TreeSet s, Object e)){
	return contains(s,e) ?  size(s) - 1: size(s);
    }

     axiom Object remove(Object clear!(TreeSet s), Object e) {
    	return false;
    }

    axiom Object remove(Object TreeSet(), Object e){
	return false;
    }
    
    // think correct
    axiom Object remove(Object remove!(TreeSet s, Object e1), Object e2) {
    	return e2.equals(e1) ? false : remove(s, e2);
    }
    
    axiom Object contains(Object remove!(TreeSet s, Object e1), Object e2) {
    	return e1.equals(e2) ? false : contains(s, e2);
    }
       
    
}
