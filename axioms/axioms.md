ArrayList (with add, get, set, and size)
=========
* `size([]) --> 0`
* `size(add!(a, e)) --> size(a)+1`
* `size(set!(a, i, e)) --> size(a)`
* `get(add!(a, e), i) --> size(a) == i ? e : get(a, i)`
* `get(set!(a, j, e), i) --> i==j ? e : get(a, i)`

ArrayList (with add, get, size, and remove)
=========
* `size([]) --> 0`
* `size(remove!(a,i)) --> size(a)-1`
* `size(add!(a,e)) --> size(a) + 1`
* `size(set!(a,i,e)) --> size(a)`
* `get(remove!(a, j), i) --> j<=i ? get(a, i+1) : get(a, i)`
* `get(add!(a, e), i) --> size(a) == i ? e : get(a, i)`
* `get(set!(a, j, e), i) --> i==j ? e : get(a, i)`

ArrayList (with add, get, set, size, remove, sort, and addAll)
=========
* `size([]) --> 0`
* `size(remove!(a,i)) --> size(a)-1`
* `size(add!(a,e)) --> size(a) + 1`
* `size(addAll!(a1, a2)) --> size(a1)+size(a2)`
* `size(sort!(a)) --> size(a)`
* `get(remove!(a, j), i) --> j<=i ? get(a, i+1) : get(a, i)`
* `get(add!(a, e), i) --> size(a) == i ? e : get(a, i)`
* `get(addAll!(a1, a2), i) --> i<size(a1) ? get(a1, i) : get(a2, i-size(a1))`
* `get(sort!(a), i) --> getSorted(a, [], [])[i]` Note: `[]` here is an empty array, not an ArrayList, and getSorted returns the sorted array
* `getSorted(add!(a,e), l, r) --> size(a) in r ? getSorted(a, l.add(e), r) : getSorted(a, l, r)`
* `getSorted(remove!(a,j), l, r) --> getSorted(a, l, r.add(j))`
* `getSorted(addAll!(a1, a2), l, r) --> getSorted(a1)+getSorted(a2)`
* `getSorted(sort!(a), l, r) --> getSorted(a, l, r)`
* `getSorted([], l, r) --> l.sort()`

Note: these axioms are slightly simplified. the `add` and `sort` methods would need to performed using logic about arrays. On that note, more arguments are needed to keep track of the current index in l and r. Also, the l array must be instantiated to the size of the array, and r must be instantiated to be the size of all of the removes from the list (I wrote a new method and accompanying axioms to compute this size).

HashMap (with put and get)
======
* `get(put!(h, k1, v), k2) --> k2==k1 ? v : get(h, k2)`
* `get([], k) --> null`

HashMap (with put, get, remove, containsKey, containsValue)
======
* `get(put!(h, k1, v), k2) --> k2==k1 ? v : get(h, k2)`
* `get([], k) --> null`
* `get(remove!(h, k1), k2) --> k2==k1 ? null : get(h, k2)`
* `containsKey(h, k) --> get(h, k) != null`
* `containsValue(put!(h, k, v1), v2) --> v2==v1 ? true : containsValue(h, v2)`
* `containsValue([], v2) --> false`
* `containsValue(remove!(h, k), v) --> containsRemove(h, v, [].add(k))`
* `containsRemove(put!(h, k, v1), v2, rs) --> k in rs ? containsRemove(h, v2, rs) : (v2==v1 ? true : containsRemove(h, v2, rs))`
* `containsRemove([], v, rs) --> false`

Note: similar to the ArrayList axioms, the size of the `rs` array would need to be determined by first calculating the number of removes (or the size) of the hashmap

HashSet
======
* `size([]) --> 0`
* `size(add!(s, e)) --> remove(s, e) ? size(s) : size(s)+1`
* `size(remove!(s, e)) --> remove(s, e) ? size(s)-1 : size(s)`
* `remove([], e) --> false`
* `remove(add!(s, e1), e2) --> e1==e2 ? true : remove(s, e2)`
* `remove(remove!(s, e1), e2) --> e2==e1 ? false: remove(s, e2)`

TreeSet
======
* `size([]) --> 0`
* `size(add!(t, e)) --> contains(t, e) ? size(t) : size(t)+1`
* `size(clear!(t)) --> 0`
* `contains([], e) --> false`
* `contains(clear!(t), e) --> false`
* `contains(add!(t, e1), e2) --> e2==e1 ? true : contains(t, e2)`

File
======
* `read(filereader(file(f, d, l, n), p)) == d[p]`
* `read!(filereader(file(f, d, l, n), p)) == filereader(file(f, d, l, n), p+1)`
* `ready(filereader(file(f, d, l, n), p)) == ITE(p != l-1, True, False)`

HashSet
=======

* `add!(add!(s, e1), e2) == ITE(e2.equals(e1), add!(s, e1), add!(add!(s, e2), e1))`
* `add(add!(s, e1), e2) == ITE(e2.equals(e1), False, add(s, e2))`
* `add([], e) == True`
* `remove!(add!(s, e1), e2) == ITE(e2.equals(e1), s, add!(remove!(s, e2), e1))`
* `remove!([], e) == []`
* `remove(add(s, e1), e2) == ITE(e2.equals(e1), True, remove(s, e2))`
* `remove([], e) == False`
* `size(add(s, _)) == size(s) + 1`
* `size([]) == 0`

TreeSet
=======

* `add!(add!(s, e1), e2) == ITE(e2.equals(e1), add!(s, e1), add!(add!(s, e2), e1))`
* `clear!(_) == []`
* `add(add!(s, e1), e2) == ITE(e2.equals(e1), False, add(s, e2))`
* `add([], e) == True`
* `contains(add!(s, e1), e2) == ITE(e2.equals(e1), True, contains(s, e2))`

ArrayDeque
==========

* `removeFirst!(addFirst!(d, e)) == d`
* `removeFirst!(addLast!(d, e)) == ITE(size(d)==0, [], addLast!(removeFirst!(d), e))`
* `removeFirst!([]) == []`
* `removeFirst(addFirst!(d, e)) == e`
* `removeFirst(addLast!(d, e)) == ITE(size(d)==0, e, removeFirst(d))`
* `removeFirst([]) == null // Note: In Java this is an exception`
* `removeLast!(addLast!(d, e)) == d`
* `removeLast!(addFirst!(d, e)) == ITE(size(d)==0, [], addFirst!(removeLast!(d), e))`
* `removeLast!([]) == []`
* `removeLast(addLast!(d, e)) == e`
* `removeLast(addFirst!(d, e)) == ITE(size(d)==0, e, removeLast(d))`
* `removeLast([]) == null // Note: In Java this is an exception`
* `peekFirst(addFirst!(d, e)) == e`
* `peekFirst(addLast!(d, e)) == ITE(size(d)==0, e, peekFirst(d))`
* `peekLast(addLast!(d, e)) == e`
* `peekLast(addFirst!(d, e)) == ITE(size(d)==0, e, peekLast(d))`
* `size(addFirst!(d, e)) == size(d) + 1`
* `size(addLast!(d, e)) == size(d) + 1`
* `size([]) == 0`
* `isEmpty(s) == ITE(size(s)==0, True, False)`

DES Example (private key -- symmetric crypto)
===========

* `let g = getInstance("DES/ECB/PKCS5Padding") in` <br />
  ` let t = doFinal(init(g, "Cipher.ENCRYPT_MODE", k1), t1) in` <br /> 
   `doFinal(init(g,"Cipher.DECRYPT_MODE", k2), t) == ITE(k2.equals(k1), t1, GARBAGE)`

RSA Example (public key -- asymmetric crypto)
=========== 

* `let g = getInstance("RSA/ECB/PKCS1Padding") in` <br />
  `let t = doFinal(init(g, "Cipher.ENCRYPT_MODE", getPublic(k1)), t1) in` <br />
   `doFinal(init(g,"Cipher.DECRYPT_MODE", getPrivate(k2)), t) == ITE(k2.equals(k1), t1, GARBAGE)`