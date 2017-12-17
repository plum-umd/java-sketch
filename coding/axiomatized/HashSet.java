class Axiom {
	harness void mn(){ }
}

/*
	?? 5 and 7
    1. add!(add!(s, e1), e2) == ITE(e2.equals(e1), add!(s, e1), add!(add!(s, e2), e1))
    2. add(add!(s, e1), e2) == ITE(e2.equals(e1), False, add(s, e2))
    3. add([], e) == True
    4. remove!(add!(s, e1), e2) == ITE(e2.equals(e1), s, add!(remove!(s, e2), e1))
    5. remove!([], e) == []
    6. remove(add(s, e1), e2) == ITE(e2.equals(e1), True, remove(s, e2))
    7. remove([], e) == False
    8. size(add!(s, _)) == size(s) + 1
    9. size([]) == 0

*/
@axiomClass
class AxHashSet{
	@adt
	Object add(Object e);

	@adt
	Object remove(Object e);

	@adt
	@pure
	int size();

	/* Not needed anymore */	
//	axiom boolean contains(Object AxHashset(), Object e)
//	{
//		return false;
//	}
        
	
	axiom Object add!(Object add!(AxHashSet h, Object e1), Object e2) // 1
	{
		return e2.equals(e1)? add!(s,e1) : add!(add!(s,e2),e1);
	}

	
	axiom Object add(Object add!(AxHashSet s, Object e1), Object e2) // 2
	{
		return e2.equals(e1)? false : add(s,e2);
	} 
	
	
	axiom Object add(Object AxHashSet(), Object e) // 3
	{
		return true;
	}
	
	axiom Object remove!(Object add!(AxHashSet s, Object e1), Object e2) // 4
	{
		return e2.equals(e1)? s : add!(remove!(s,e2), e1);
	}
	
	// ??remove!([], e) == []
	axiom Object remove!(Object AxHashSet(), Object e) // 5
	{
		return new AxHashSet();
	}
	
	/* remove(add(s, e1), e2) == ITE(e2.equals(e1), True, remove(s, e2))*/
	axiom Object remove(Object add(AxHashSet s, Object e1), Object e2) // 6
	{
		return e2.equals(e1) ? true : remove(s, e2);
	}

	// remove([], e) == false
	
	axiom Object remove(Object AxHashSet(), Object e) // 7
	{
		return false;
	}

	/* size(add(s, _)) == size(s) + 1 */
	// axiom Object size(Object add(AxHashSet s, Object e))
	axiom Object size(Object add!(AxHashSet s, Object e)) // 8
	{	
		return size(s.self) + 1;
	}
	// Need to make sure size(s) and size(s.self)

	axiom Object size(Object AxHashSet()) // 9
	{
		return 0;
	}
	
}
