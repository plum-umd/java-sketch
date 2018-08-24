@rewriteClass
class ArrayList {
    @alg
    // boolean add(Object e);
    Object add(Object e);

    @alg
    Object set(int i, Object e);

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
}
