@axiomClass
class HashMap<K, V> {

    @adt
    Object put(Object k, Object v);

    @adt
    Object remove(Object k);
    
    @adt
    @pure
    Object get(Object k);

    @adt
    @pure
    boolean containsKey(Object k);

    @adt
    Object clear();

    // axiom Object put(Object HashMap(), Object k, Object v) {
    // 	return null;
    // }

    // axiom Object put(Object put!(HashMap h, Object k1, Object v1), Object k2, Object v2) {
    // 	return k2.equals(k1) ? v1 : put(h, k2, v2);
    // }

    axiom Object get(Object remove!(HashMap h, Object k1), Object k2) {
    	return k2.equals(k1) ? null : get(h, k2);
    }
    
    axiom Object get(Object put!(HashMap h, Object k1, Object v1), Object k2) {
	return k2.equals(k1) ? v1 : get(h, k2);
    }

    axiom Object get(Object HashMap(), Object k) {
	return null;
    }

    axiom Object containsKey(Object remove!(HashMap h, Object k1), Object k2) {
    	return k2.equals(k1) ? false : containsKey(h, k2);
    }
    
    axiom Object containsKey(Object put!(HashMap h, Object k1, Object v1), Object k2) {
	return k1.equals(k2) ? true : containsKey(h, k2);
    }

    axiom Object containsKey(Object HashMap(), Object k) {
	return false;
    }

    axiom Object get(Object clear!(Hashmap h), Object k)
    {
	return null;
    }

	
    
      
}
