@rewriteClass
class ArrayList<E>{
    @alg
    // boolean add(E e);
    Object add(E e);

    @alg
    @pure
    E get(int i);

    @alg
    E set(int i, E e);

    @alg
    @pure
    void ensureCapacity(int n);
    
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
	// return size(a) == i-1 ? e1 : get(a, i);
	return size(a) == i ? e1 : get(a, i);
    }

    rewrite Object get(Object set!(ArrayList a, int j, Object e), int i) {
	return i==j ? e : get(a, i);
    }

    // rewrite Object get(Object ArrayList(), int i) {
    // 	return null;
    // }
}
