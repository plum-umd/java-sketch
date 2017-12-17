class Axiom {
    harness void mn() { }
}

/*

   1. put!(put!(h, k1, v1), k2, v2) == ITE(k2.equals(k1), put!(h, k2, v2), put!(put!(h, k2, v2), k1, v1))
   2. put(put!(h, k1, v1), k2, v2) == ITE(k2.equals(k1), v1, put(h, k2, v2))
   3. put([], k, v) == null
   4. get(put!(h, k1, v), k2) == ITE(k2.equals(k1), v, get(h, k2))
   5. get([], k2) == null
   6. remove!(put!(h, k1, v), k2) == ITE(k2.equals(k1), h, put!(remove!(h, k2), k1, v))
   7. remove!([], k) == []
   8. remove(put!(h, k1, v), k2) == ITE(k2.equals(k1), v, remove(h, k2))
   9. remove([], k) == null
   10. containsKey(put!(h, k1, v), k2) == ITE(k2.equals(k1), True, containsKey(h, k2))
   11. containsKey([], k) == False
   12. containsValue(put!(h, k, v1), v2) == ITE(v2.equals(v1), True, containsValue(h, v2))
   13. size(put!(h, _, _)) == size(h) + 1
   14. size([]) == 0

*/

@axiomClass
class AxHashMap{
	@adt
	Object put(Object key, Object value)
//	Object put(AxHashMap h, Object key, Object value)

	@adt
	@pure
	int size()
//	Object size(AxHashMap h)

	@adt
	@pure
	Object get(Object key)
//	Object get(AxHashMap h, Object key)
	
	@adt
	@pure
	boolean containsKey(Object key)
//	boolean containsKey(AxHashMap h, Object key)

	@adt
	@pure
	boolean containsValue(Object value)
//	boolean containsValue(AxHashMap h, Object value)
	

	//1
	axiom Object put!(Object put!(AxHashMap h, Object k1, Object v2), Object k2, Object v2)
	{
		return k2.equals(k1)? put!(h,k2,v2) : put!(put!(h,k2,v2),k1,v1);
	}

	//2
	axiom Object put(Object put!(AxHashMap h, k1, v1), Object k2, Object v2)
	{
		return k2.equals(k1) ? v1 : put(h,k2,v2); 
	}
	
	// 3
	// put([], k, v) == null
	// should return true??
	axiom Object put(Object AxHashMap(), Object k, Object v)
	{
		return true;
	} 

	// 4
	axiom Object get(Object put!(AxHashMap h, Object k1, Object v), Object k2)
	{
		return k2.equals(k1)? v : get(h, k2);
	}

	// 5 returning null???????
	axiom Object get(Object AxHashMap(), Object k2)
	{
		return null;
	}

	// 6
	axiom Object remove!(Object put!(AxHashMap h, Object k1, Object v), Object k2)
	{
		return k2.equals(k1) ? h : put!(remove!(h, k2), k1, v); 
	}
	
	// not sure ?? To new an Object
	axiom Object remove!(Object AxHashMap(), Object k1)
	{
		return new AxHashMap();
	}

	// 8 Again why?
	axiom remove(Object AxHashMap(), Object k)
	{
		return null;
	}

	//9
	axiom Object containsKey(Object put!(AxHashMap h, Object k1), Object v2)
	{
		return k2.equals(k1) ? true : containsKey(h, k2);
	}

	//10
	axiom Object containsKey(Object AxHashMap(), Object k)
	{
		return false;
	}

	//11
	axiom Object containsKey(Object put!(AxHashMap h, Object k, Object v1), Object k2)
	{
		return k2.equals(k1) ? true : containsKey(h, k2);
	}

	//12
	axiom Object containsKey(Object AxHashMap(), Object k)
	{
		return false;
	}

	// 13
	axiom Object containsValue(Object put!(AxHashMap h, Object k, Object v1), Object v2)
	{
		return v2.equals(v1) ? true : containsValue(h, v2);
	}
	
	// 14??Correct ?? h.self??
	axiom Object size(Object put!(AxHashMap h, Object k, Object v))
	{
		return size(h) + 1;
	}

	axiom Object size(Object AxHashMap())
	{
		return 0;
	}
}
