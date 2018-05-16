@axiomClass
class TreeSet {

    @adt
    boolean add(Integer e);
    
    @adt
    Object clear();

    @adt
    @pure
    boolean contains(Integer e);

    @adt
    @pure
    int size();

    @adt
    @pure
    Integer last();
    
    @adt
    boolean remove(Integer e);

    axiom Object size(Object TreeSet()) {
    	return 0;
    }

    axiom Object size(Object add!(TreeSet s, Integer e)) {
    	return contains(s, e) ? size(s) : size(s)+1;
    }

    axiom Object size(Object clear!(TreeSet s)) {
    	return 0;
    }
    
    axiom Object add(Object clear!(TreeSet s), Integer e) {
    	return true;
    }
    
    axiom Object add(Object TreeSet(), Integer e) {
    	return true;
    }

    axiom Object add(Object add!(TreeSet s, Integer e1), Integer e2) {
    	return e2.equals(e1) ? false : add(s, e2);
    }

    axiom Object contains(Object add!(TreeSet s, Integer e1), Integer e2) {
    	return e1.equals(e2) ? true : contains(s, e2);
    }

    axiom Object contains(Object TreeSet(), Integer e) {
    	return false;
    }

    axiom Object contains(Object clear!(TreeSet s), Integer e) {
    	return false;
    }
    
    axiom Object last(Object add!(TreeSet s, Integer e1))
    {
    	Integer tmp = last(s);
    	return tmp.compareTo(e1) > 0 ? tmp : e1;
    }

    axiom Object size(Object remove!(TreeSet s, Integer e)){
    	return contains(s,e) ?  size(s) - 1: size(s);
    }

     axiom Object remove(Object clear!(TreeSet s), Integer e) {
    	return false;
    }

    axiom Object remove(Object TreeSet(), Integer e){
    	return false;
    }
    
    // // think correct
    // axiom Object remove(Object remove!(TreeSet s, Object e1), Object e2) {
    // 	return e2.equals(e1) ? false : remove(s, e2);
    // }
    
    // axiom Object contains(Object remove!(TreeSet s, Object e1), Object e2) {
    // 	return e1.equals(e2) ? false : contains(s, e2);
    // }
       
    
}
