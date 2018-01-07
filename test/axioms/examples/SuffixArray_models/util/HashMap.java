@axiomClass
class HashMap {

    @adt
    Object put(Object k, Object v);

    @adt
    @pure
    Object get(Object k);

    axiom Object put(Object HashMap(), Object k, Object v) {
	return null;
    }

    axiom Object put(Object put!(HashMap h, Object k1, Object v1), Object k2, Object v2) {
	return k2.equals(k1) ? v1 : put(h, k2, v2);
    }

    axiom Object get(Object put!(HashMap h, Object k1, Object v1), Object k2) {
	return k2.equals(k1) ? v1 : get(h, k2);
    }

    axiom Object get(Object HashMap(), Object k) {
	return null;
    }
}
