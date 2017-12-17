class Axiom {
	harness void mn(){ }
}


/*  Axioms to implement
	
    1. add!(add!(s, e1), e2) == ITE(e2.equals(e1), add!(s, e1), add!(add!(s, e2), e1))
    2. clear!(_) == []
    3. add(add!(s, e1), e2) == ITE(e2.equals(e1), False, add(s, e2))
    4. add([], e) == True
    5. contains(add!(s, e1), e2) == ITE(e2.equals(e1), True, contains(s, e2))

*/
@axiomClass
class AxTreeSet{
	@adt
	Object add(Object e)
	
	@adt
	Object clear()

	@adt
	boolean contains(Object e)

	axiom Object add!(Object add!(AxTreeSet t, Object e1), Object e2) // 1
	{
		return e2.equals(e1)? add!(s,e1) : add!(add!(s,e2),e1);
	}

	axiom Object clear!(AxTreeSet t)	// 2
	{
		return Object AxTreeSet();
	}
	
	axiom Object add(Object add!(AxTreeSet s, Object e1), Object e2) // 3
	{
    	 	return e2.equals(e1) ? false : add(s, e2);
    	}

	axiom Object add(Object AxTreeSet(), Object e) // 4
	{
		return true;
	}

	axiom Object contains(Object add!(AxTreeSet s, Object e1), Object e2) // 5
	{
		return e2.equals(e1) : true : contains(s,e2);
	}

	
}
