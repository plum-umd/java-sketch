@rewriteClass
// class ArrayList<E> implements List<E>{
class ArrayList<E> {
    @alg
    // boolean add(Object e);
    Object add(Object e);

    @alg
    @pure
    Object get(int i);

    @alg
    Object set(int i, Object e);

    @alg
    @pure
    void ensureCapacity();
    
    @alg
    @pure
    int size();

    rewrite Object size(Object ArrayList()) {
    	return 0;
    }

    rewrite Object size(Object add!(ArrayList a, Object e)) {
    	return size(a)+1;
    }

    rewrite Object size(Object set!(ArrayList a, int i, Object e)) {
    	return size(a);
    }

    rewrite Object get(Object add!(ArrayList a, Object e1), int i) {
	int sz = size(a);
    	return (sz == i) ? e1 : get(a, i);
    }

    rewrite Object get(Object set!(ArrayList a, int j, Object e), int i) {
    	return i==j ? e : get(a, i);
    }
}
