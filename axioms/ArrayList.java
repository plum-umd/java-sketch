@axiom // lets compiler know this is an adt
class ArrayList {
    // Gave names to the parameters so we can specify names for the adt fields here
    @adt  // constructor in adt
    Object get(int i);

    // I think we only need set if we have an axiom where we're worried
    // about the return value from set
    @adt
    Object set(int i, Object o);
    @adt  // constructor in adt
    Object set!(int i, Object o);

    @axiom // this should be used to fill in xform
    Object get(set!(ArrayList a, int i, Object o), int j) => i == j ? o : get(a, j);
    // or
    @axiom
    Object get(set!(ArrayList a, int i, Object o), int j) { return i == j ? o : get(a, j); }
}
/*
 * Every constructor in adt has field of its own type?
 
  @axiom
  class ArrayList { } =>
  adt ArrayList { }

  @adt
  Object get(int); =>
  adt ArrayList {
    Get { ArrayList a; int i; } }

  @adt
  Object set(int); =>
  adt ArrayList {
    Get { ArrayList a; int i; }
    Set { ArrayList a; int i; Object o; } }

  @adt
  Object set!(int); =>
  adt ArrayList {
    Get  { ArrayList a; int i; }
    Set  { ArrayList a; int i; Object o; }
    SetB { ArrayList a; int i; Object o; } }
    
  @axiom
  Object get(set!(ArrayList a, int i, Object o), int j) => i == j ? o : get(a, j); =>
  // We assume this is getting called on the `a` in a get(a, _)
  xform_get(ArrayList a, int j) {
    switch(a) {
    // since get is the first method in the axiom if fires on this case
    case Get:  assert fail; // No axioms for get(get(_))
    case Set:  assert fail; // No axioms for get(set(_))
    case SetB: { // since we are in the set 
      if (a.i == j) return a.o;
      else return xform_get(a.a, j);
      }
    }
  }

*/
  
