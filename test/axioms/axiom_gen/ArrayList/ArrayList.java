@rewriteClass
class ArrayList {
    @alg
    Object add(Object e);

    @alg
    @pure
    int size();

    rewrite Object size(Object ArrayList()) {
    	return 0;
    }

    rewrite Object size(Object add!(ArrayList a, Object e)) {
    	return size(a)+1;
    }
}
