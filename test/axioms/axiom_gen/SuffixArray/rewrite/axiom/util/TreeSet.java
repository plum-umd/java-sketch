@rewriteClass
class TreeSet {

    @alg
    // boolean add(Object e);
    Object add(Object e);
    
    @alg
    Object clear();

    @alg
    @pure
    boolean contains(Object e);

    @alg
    @pure
    int size();

    rewrite Object size(Object TreeSet()) {
	return 0;
    }

    rewrite Object size(Object add!(TreeSet s, Object e)) {
	boolean b = contains(s, e);
	if (b) {
	    return size(s);
	} else {
	    return size(s)+1;
	}
	// return contains(s, e) ? size(s) : size(s)+1;
    }

    rewrite Object size(Object clear!(TreeSet s)) {
	return 0;
    }
    
    // rewrite Object add(Object clear!(TreeSet s), Object e) {
    // 	return true;
    // }
    
    // rewrite Object add(Object TreeSet(), Object e) {
    // 	return true;
    // }

    // rewrite Object add(Object add!(TreeSet s, Object e1), Object e2) {
    // 	return e2.equals(e1) ? false : add(s, e2);
    // }

    rewrite Object contains(Object add!(TreeSet s, Object e1), Object e2) {
    	return e1.equals(e2) ? true : contains(s, e2);
    }

    rewrite Object contains(Object TreeSet(), Object e) {
	return false;
    }

    rewrite Object contains(Object clear!(TreeSet s), Object e) {
    	return false;
    }

}
