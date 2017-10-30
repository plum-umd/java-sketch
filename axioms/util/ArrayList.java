@axiomClass
class ArrayList {
    @adt
    boolean add(Object e);

    @adt
    Object get(int i);

    @adt
    @pure
    int size();

    axiom Object size(Object ArrayList()) {
	return 0;
    }

    axiom Object size(Object add!(ArrayList a, Object e)) {
	return size(a)+1;
    }

    axiom Object get(Object add!(ArrayList a, Object e1), int i) {
	return size(a) == i-1 ? e1 : get(a, i);
    }
}
