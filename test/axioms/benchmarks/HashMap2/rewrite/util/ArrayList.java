@rewriteClass
class ArrayList {
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
    void ensureCapacity(int n);
    
    @alg
    @pure
    int size();

    @alg
    Object remove(int i);

    rewrite Object size(Object ArrayList()) {
	return 0;
    }

    rewrite Object size(Object remove!(ArrayList a, int i)) {
	return size(a)-1;
    }
    
    rewrite Object size(Object add!(ArrayList a, Object e)) {
	return size(a)+1;
    }

    rewrite Object size(Object set!(ArrayList a, int i, Object e)) {
	return size(a);
    }

    rewrite Object get(Object remove!(ArrayList a, int j), int i) {
	return i==j ? null : get(a, i);
    }
    
    rewrite Object get(Object add!(ArrayList a, Object e1), int i) {
	return size(a) == i-1 ? e1 : get(a, i);
    }

    rewrite Object get(Object set!(ArrayList a, int j, Object e), int i) {
	return i==j ? e : get(a, i);
    }

    rewrite Object get(Object ArrayList(), int i) {
	return null;
    }
}
