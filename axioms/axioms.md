String
======
(`length < toUpper < replace < substring < concat < null`)
* `length(toUpper(s)) == length(s)`
* `length(replace(s1, c1, c2)) == length(s1)`
* `length(substring(s, i, j)) == MAX(j - i, 0)`
* `length(concat(s1,s2)) == length(s1) + length(s2)`
* `length(null) == 0`
* `toUpper(replace(s1, c1, c2)) == replace(toUpper(s1), toUpper(c1), toUpper(c2))`
* `toUpper(substring(s, i, j)) == substring(toUpper(s), i, j)`
* `toUpper(concat(s1, s2)) == concat(toUpper(s1), toUpper(s2))`
* `toUpper(null) == null`
* `replace(substring(s, i, j), c1, c2) == substring(replace(s, c1, c2), i, j)`
* `replace(concat(s1, s2), c1, c2) == concat(replace(s1, c1, c2), replace(s2, c1, c2))`
* `replace(null, c1, c2) = null`
* `substring(concat(s1, s2), i, j) == concat(substring(s1, i, j), substring(s2, i-length(s1), j-length(s2)))`
* `substring(null, i, j)` == null
* `concat(null, s2) == s2`
* `concat(s1, null) == s1`

* `split(s1, s2).length <= length(s1) // inequality? are we ready for these?`
* `toString(s) == s // boring…but maybe somehow a useful axiom`
* `compareTo(f(s1), f(s2)) == compareToIgnoreCase(s1,s2) where f=to[Upper|Lower]Case(s))`
* `length(s) >= ITE(s == null, 0, 1)`

Stack:
=======
(`isEmpty < size < pop,peek < push`)
* `isEmpty(x) == (size(x) == 0)`
* `size(pop(x)) == MAX(size(x),1) - 1 // size inherited from Vector`
* `size(push(x)) == size(x) + 1 // size inherited from Vector`
* `pop(push(s, x)) == x`
* `peek(push(x)) == x`
* `size(s) >= ITE(s == null, 0, 1)`

HashMap:
=======
* `get(add(x, a), i) == ITE(length(x) == i-1, a, get(x, i))`
* `get(set(x, a, j), i) == ITE(i == j, a, get(x, i))`
* `put(h, k, v) == v`
* `get(put(h, k, v), k) == v`
* `get(clone(h), k) == get(h, k)`
* `put(clone(h), k, v) == put(h, k, v)`
* `isEmpty(put(h, k, v)) == False`
* `remove(put(h, k, v), k) == v // V remove(Object key)`
* `remove(put(h, k, v), k, v) == True // boolean remove(Object key, Object value)`
* `replace(put(h, k, v1), k, v2) == v1 V // replace(Object key)`
* `replace(put(h, k, v1), k, v1, v2) == True // boolean replace(Object key, Object old_value, Object new_value)`
* `remove(put(put(h, k1, v1), k2, v2), k1) == v1`
* `remove(put(put(h, k1, v1), k2, v2), k2) == v2`
* `get(remove(put(h, k, v), k), k) == null`
* `get(remove(put(put(h, k1, v1), k2, v2), k2), k1) == v1`
* `get(remove(put(put(h, k1, v1), k2, v2), k1), k2) == v2`
* `containsKey(put(h, k, v), k) == True`
* `containsKey(remove(put(h, k, v), k), k) == False`
* `containValue(put(h, k, v), v) == True`
* `containValue(remove(put(h, k, v), k), v) == False`
* `isEmpty(h) => size(h) == 0`
* `!isEmpty(h) => size(h) > 0`
* `h == null => size(h) == 0`
* `h != null => size(h) > 0`

ArrayList:
=========
* `add(clone(a), e) == add(a, e) // and other clone stuff`
* `add(a, e) == True // and other clone stuff`
* `isEmpty(add(a, e)) == False`
* `contains(add(a, e), e) == True`
* `contains(remove(add(a, e), e), e) == False`
* `get(set(a, i, e), e) == e`
* `indexOf(remove(add(a, e), e), e) == -1`
* `remove(add(a, v), v) == True`
* `size(add(a, e)) == size(a) + 1`
* `size(replaceAll(a, op)) == size(a)`
* `size(sort(a)) == size(a)`
* `isEmpty(a) => size(a) == 0`
* `!isEmpty(a) => size(a) > 0`
* `a == null => size(a) == 0`
* `a != null => size(a) > 0`
* `remove(a, e) == True => size(a) > 0 // not sure about this`
* `remove(a, e) == True => size(remove(a, e)) == size(a) - 1 // not sure about this`

ArrayDeque:
=========

* `getFirst(a) == getFirst(a, 0, 0)`
* `getFirst([], n, m) == null`
* `getFirst(addFirst(a, e), n, m) == ITE(n > 0, getFirst(a, n-1, m), ITE(n+m == size(e), null, e))`
* `getFirst(addLast(a, e), n, m) == ITE(size(a) == 0, ITE(m == 1, null, e), getFirst(a,n,m-1))`
* `getFirst(removeFirst(a), n, m) == getFirst(a, n+1, m)`
* `getFirst(removeLast(a), n, m) == getFirst(a, n, m+1)`