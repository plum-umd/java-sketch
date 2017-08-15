class Axiom {
    harness void mn() { }
}

@axiomClass
class AxArrayList {
    @adt
    @pure
    Object get(int i);

    @adt
    Object add(Object o);

    @adt
    Object set(int i, Object o);

    @adt
    @pure
    int size();
    
    axiom Object get(Object add!(AxArrayList a, Object o), int j) {
    	return size(a) == j-1 ? o : get(a.self, j);
    }
    axiom Object get(Object set!(AxArrayList a, int i, Object o), int j) {
    	return i == j ? o : get(a.self, j);
    }
    axiom Object size(Object AxArrayList()) {
    	return 0;
    }
    axiom Object size(Object add!(AxArrayList a, Object o)) {
    	return size(a.self) + 1;
    }
    axiom Object size(Object set!(AxArrayList a, int i, Object o)) {
    	return size(a.self);
    }
}
    
    // axiom Object get(Object set!(Object add!())) { return x; }
    // axiom Object get(int set!(ArrayList a, int i, Object o), int j) { return i == j ? o : get(a, j); }
