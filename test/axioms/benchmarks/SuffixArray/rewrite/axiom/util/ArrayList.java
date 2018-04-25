@rewriteClass
class ArrayList {
    @alg
    boolean add(Object e);

    @alg
    Object get(int i);

    @alg
    @pure
    int size();

    rewrite Object size(Object ArrayList()) {
	return 0;
    }

    rewrite Object size(Object add!(ArrayList a, Object e)) {
	return size(a)+1;
    }

    rewrite Object get(Object add!(ArrayList a, Object e1), int i) {
	return size(a) == i-1 ? e1 : get(a, i);
    }
}
