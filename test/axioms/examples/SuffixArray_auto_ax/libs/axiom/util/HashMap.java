@rewriteClass
class HashMap {

    @alg
    Object put(Object k, Object v);

    @alg
    @pure
    Object get(Object k);

    rewrite Object put(Object HashMap(), Object k, Object v) {
	return null;
    }

    rewrite Object put(Object put!(HashMap h, Object k1, Object v1), Object k2, Object v2) {
	return k2.equals(k1) ? v1 : put(h, k2, v2);
    }

    rewrite Object get(Object put!(HashMap h, Object k1, Object v1), Object k2) {
	return k2.equals(k1) ? v1 : get(h, k2);
    }

    rewrite Object get(Object HashMap(), Object k) {
	return null;
    }
}
