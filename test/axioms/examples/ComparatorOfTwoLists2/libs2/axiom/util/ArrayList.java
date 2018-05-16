@axiomClass
// class ArrayList<E> implements List<E>{
class ArrayList<E> {
    @adt
    boolean add(Object e);

    @adt
    @pure
    Object get(int i);

    @adt
    Object set(int i, Object e);

    @adt
    @pure
    void ensureCapacity();
    
    @adt
    @pure
    int size();

    @adt
    void sort(Object t);

    @adt
    @pure
    Object getIthBiggest(Object os, int i);

    @adt
    void remove(int i);

    @adt
    void addAll(Object a);
    
    axiom Object size(Object ArrayList()) {
    	return 0;
    }

    axiom Object size(Object add!(ArrayList a, Object e)) {
    	return size(a)+1;
    }

    axiom Object size(Object set!(ArrayList a, int i, Object e)) {
    	return size(a);
    }

    // axiom Object size(Object remove!(ArrayList a, int i)) {
    // 	return size(a)-1;
    // }

    // axiom Object get(Object addAll(ArrayList a1, ArrayList a2), int i) {
    // 	int l1 = size(a1);
    // 	if (i < l1) { return get(a1, i); }
    // 	i = i - l1;
    // 	return get(a2, i);
    // }
    
    // axiom Object get(Object ArrayList(), int i) {
    // 	return null;
    // }
    
    // axiom Object get(Object remove!(ArrayList a, int j), int i) {
    // 	return (j <= i) ? get(a, i+1) : get(a, i);
    // }
    
    axiom Object get(Object add!(ArrayList a, Object e1), int i) {
	int sz = size(a);
    	return (sz == i) ? e1 : get(a, i);
    }

    axiom Object get(Object set!(ArrayList a, int j, Object e), int i) {
    	return i==j ? e : get(a, i);
    }

    axiom Object get(Object sort!(ArrayList a, Object t), int i) {
    	// int length = size(a);
    	// Object[] os2 = new Object[length];
	Object rs = null;
    	// return getIthBiggest(a, os2, i);
	return getIthBiggest(a, rs, i);
    }

    // axiom Object getIthBiggest(Object add!(ArrayList a, Object e1), Object os, int i) {
    // 	// int sz = size(a);
    // 	// return (sz == i) ? e1 : get(a, i);
    // }

    // axiom Object getIthBiggest(Object set!(ArrayList a, int j, Object e), Object os, int i) {
    // 	// int sz = size(a);
    // 	// return (sz == i) ? e1 : get(a, i);
    // }
    
}
