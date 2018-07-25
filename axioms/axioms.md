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

ArrayDeque
=========
* `size([]) --> 0`
* `size(addLast!(d, e)) --> size(d)+1`
* `size(addFirst!(d, e)) --> size(d)+1`
* `size(removeFirst!(d)) --> size(d)-1`
* `size(removeLast!(d)) --> size(d)-1`
* `peekLast([]) --> null`
* `peekLast(addLast!(d, e)) --> e`
* `peekLast(addFirst!(d, e)) --> size(d)==0 ? e : peekLast(d)`
* `peekLast(removeLast!(d, e)) --> peekLastCount(d, 0, 1)`
* `peekLast(removeFirst!(d, e)) --> peekLastCount(d, 1, 0)`
* `peekLastCount([], i, j) --> null`
* `peekLastCount(addLast!(d, e), i, j) --> j>0 ? peekLastCount(d, i, j-1) : (i>0 ? (size(d)==i ? null : e) : e)`
* `peekLastCount(addFirst!(d, e), i, j) --> size(d)==0 && i==0 && j==0 ? e : (i>0 ? peekLastCount(d, i-1, j) : (size(d)==j ? null : peekLastCount(d, i, j))) 
* `peekLastCount(removeFirst!(d), i , j) --> peekLastCount(d, i+1, j)`
* `peekLastCount(removeLast!(d), i, j) --> peekLastCount(d, i, j+1)`

Note: peekFirst would be very similar to peekLast

Cipher (with init and doFinal (one arg))
=====
* `doFinal(init!(c1, m1, k1), doFinal(init!(c2, m2, k2), t)) --> ` <br />
  `m1==DEC && m2 == ENC && k1.equals(k2) ? t : GARBAGE`

Note: The benchmarks we used with Cipher varied a bit in the versions of `doFinal` used (i.e. how many args passed), however, all of the axioms for Cipher were similar to this.

Mac
==
* `doFinal(init!(m, s), t) --> t`

BufferedReader
=============
* `readLine([f]) --> f.getLine(0)`
* `readLine(readLine!(b)) --> readLineCount(b, 1)`
* `readLineCount([f], i) --> f.getLine(i)`
* `readLineCount(readLine!(b), i) --> readLineCount(b, i+1)`

