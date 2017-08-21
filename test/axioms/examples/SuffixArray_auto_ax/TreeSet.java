class TreeSet {
    harness void mn() { }   
}

@axiomClass
class AxTreeSet {

    @adt
    boolean add(Object e);
    
    @adt
    Object clear();

    @adt
    boolean contains(Object e);

    // Doesn't compile b/c it's a bang axiom (bang in name && ADT return)
    // axiom Object add!(Object add!(AxTreeSet t, Object e1), Object e2) {
    // 	return e2.equals(e1) ? (Object add!(AxTreeSet t, Object e1)) : (Object add!(Object add!(AxTreeSet t, Object e1), Object e2));
    // }

    // Compiles but type probs (no boxing/unboxing of boolean type)
    axiom Object add(Object AxTreeSet(), Object e) {
	return true;
    }

    // Doesn't compile due to recursive add "call"
    // axiom Object add(Object add!(AxTreeSet s, Object e1), Object e2) {
    // 	return e2.equals(e1) ? false : add(s, e2);
    // }

    // Doesn't compile due to recursive add "call"    
    // axiom Object contains(Object add!(AxTreeSet s, Object e1), Object e2) {
    // 	return e2.equals(e1) ? true : contains(s, e2);
    // }

    // Doesn't compile b/c it's a bang axiom
    // axiom clear!(AxTreeSet s) {
    // 	return Object AxTreeSet();
    // }
}
