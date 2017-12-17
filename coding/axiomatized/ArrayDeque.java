class Axiom {
    harness void mn() { }
}

/*

   1 removeFirst!(addFirst!(d, e)) == d
   2 removeFirst!(addLast!(d, e)) == ITE(size(d)==0, [], addLast!(removeFirst!(d), e))
   3 removeFirst!([]) == []
   4 removeFirst(addFirst!(d, e)) == e
   5 removeFirst(addLast!(d, e)) == ITE(size(d)==0, e, removeFirst(d))
   6 removeFirst([]) == null // Note: In Java this is an exception
   7 removeLast!(addLast!(d, e)) == d
   8 removeLast!(addFirst!(d, e)) == ITE(size(d)==0, [], addFirst!(removeLast!(d), e))
   9 removeLast!([]) == []
*/


@axiomClass
class AxArrayDeque{
	@adt
	Object removeFirst()
	
	@adt
	Object addFirst()
	
	@adt
	Object removeLast()

	@adt
	Object removeFirst()

	@adt
	@pure
	Object peekFirst()

	@adt
	@pure
	Object peekLast()

	@adt
	@pure
	int size()

	@adt
	@pure
	boolean isEmpty(AxArrayDeque d)

	//1
	axiom Object removeFirst!(Object addFirst!(AxArrayDeque d, Object e))	
	{
		return d;
	}
	
	//2
	axiom Object removeFirst!(Object addLast!(AxArrayDeque d, Object e))	s
	{
		return size(d) == 0 ? new AxArrayDeque() : addLast!(removeFirst!(d,e));
	}

	//3
	axiom Object removeFirst!(Object AxArrayDeque())
	{
		return new AxArrayDeque();
	}

	//4
	axiom Object removeFirst(Object addFirst!(AxArrayDeque d, Object e))
	{
		return e;
	}
	
	//5
	axiom Object removeFirst(Object addLast!(d,e))
	{
		return size(d) == 0 ? e : removeFirst(d);
	}

	//6
	axiom Object removeFirst(Object AxArrayDeque())
	{
		return null;
	}

	//7
	axiom Object removeLast!(Object addLast!(AxArrayDeque d, Object e))
	{
		return d;
	}

	//8
	axiom Object removeLast!(Object addFirst!(AxArrayDeque d, Object e))
	{
		return size(d) == 0? new AxArrayDeque() : addFirst!(removeLast!(d,e));
	}

	//9
	axiom Object removeLast!(Object AxArrayDeque())
	{
		return new AxArrayDeque();
	}

	
/*
  10  removeLast(addLast!(d, e)) == e
  11  removeLast(addFirst!(d, e)) == ITE(size(d)==0, e, removeLast(d))
  12  removeLast([]) == null // Note: In Java this is an exception
  13  peekFirst(addFirst!(d, e)) == e
  14  peekFirst(addLast!(d, e)) == ITE(size(d)==0, e, peekFirst(d))
  15  peekLast(addLast!(d, e)) == e
  16  peekLast(addFirst!(d, e)) == ITE(size(d)==0, e, peekLast(d))
  17  size(addFirst!(d, e)) == size(d) + 1
  18  size(addLast!(d, e)) == size(d) + 1
  19  size([]) == 0
  20  isEmpty(d) == ITE(size(d)==0, True, False)??
*/

	//10
	axiom Object removeLast(Object addLast!(AxArrayDeque d, Object e))
	{
		return e;
	}

	//11
	axiom Object removeLast(Object addFirst!(AxArrayDeque d, Object e))
	{
		return size(d) == 0 ? e : removeLast(d);
	}
	
	//12
	axiom Object removeLast(Object AxArrayDeque())
	{
		return null;
	}

	//13
	axiom Object peekFirst(Object addFirst!(AxArrayDeque d, Object e))
	{
		return e;
	}

	//14
	axiom Object peekFirst(Object addLast!(AxArrayDeque d, Object e))
	{
		return size(d) == 0 ?  e : peekFirst(d);
	}
	
	//15
	axiom Object peekLast(Object addLast!(AxArrayDeque d, Object e))
	{
		return e;
	}
	
	//16
	axiom Object peekLast(Object addFirst!(AxArrayDeque d, Object e))
	{
		return size(d) == 0 ?  e : peekLast(d);
	}

	//17
	axiom Object size(Object addFirst!(AxArrayDeque d, Object e))
	{
		return size(d) + 1;
	}


	//18
	axiom Object size(Object addLast!(AxArrayDeque d, Object e))
	{
		return size(d) + 1;
	}

	//19
	axiom Object size(Object AxArrayDeque ())
	{
		return 0;
	}

	//20
	axiom isEmpty(AxArrayDeque d)
	{
		return size(d) == 0 : true ? false;
	}
}
