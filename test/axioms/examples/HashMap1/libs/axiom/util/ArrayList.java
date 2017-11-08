@axiomClass
class ArrayList {
    @adt
    boolean add(Object e);

    @adt
    Object get(int i);

    @adt
    Object set(int i, Object e);

    @adt
    @pure
    void ensureCapacity(int n);
    
    @adt
    @pure
    int size();

    axiom Object size(Object ArrayList()) {
	return 0;
    }

    axiom Object size(Object add!(ArrayList a, Object e)) {
	return size(a)+1;
    }

    axiom Object size(Object set!(ArrayList a, int i, Object e)) {
	return size(a);
    }

    axiom Object get(Object add!(ArrayList a, Object e1), int i) {
	return size(a) == i-1 ? e1 : get(a, i);
    }

    axiom Object get(Object set!(ArrayList a, int j, Object e), int i) {
	return i==j ? e : get(a, i);
    }
}
