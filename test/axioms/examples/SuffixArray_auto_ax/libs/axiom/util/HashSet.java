@rewriteClass
class HashSet {

    @alg
    boolean add(Object e2);

    @alg
    boolean remove(Object e2);

    @alg
    @pure
    int size();

    rewrite Object add(Object HashSet(), Object e) {
    	return true;
    }

    rewrite Object add(Object add!(HashSet h, Object e1), Object e2) {
    	return e2.equals(e1) ? false : add(h, e2);
    }

    rewrite Object remove(Object HashSet(), Object e) {
    	return false;
    }

    rewrite Object remove(Object add!(HashSet h, Object e1), Object e2) {
    	return e2.equals(e1) ? true : remove(h, e2);
    }

    rewrite Object remove(Object remove!(HashSet h, Object e1), Object e2) {
    	return e2.equals(e1) ? false : remove(h, e2);
    }

    rewrite Object size(Object HashSet()) {
    	return 0;
    }
    
    rewrite Object size(Object add!(HashSet h, Object e1)) {
    	return size(h) + 1;
    }

    rewrite Object size(Object remove!(HashSet h, Object e1)) {
	boolean b = remove(h, e1);
	if (b) {
	    return size(h)-1;
	} else {
	    return size(h);
	}
	// return remove(h, e1) ? size(h)-1 : size(h);
    }
}
