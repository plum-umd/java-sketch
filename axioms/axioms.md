String
======
* `length(concat(s1,s2)) == length(s1) + length(s2)`
* `length(replace(s1, c1, c2)) == length(s1)`
* `length(substring(s, i, j)) == j - i`
* `split(s1, s2).length <= length(s1) // inequality? are we ready for these?`
* `length(toUpper(s)) == length(s)`
* `toString(s) == s // boring…but maybe somehow a useful axiom`
* `compareTo(f(s1), f(s2)) == compareToIgnoreCase(s1,s2) where f=to[Upper|Lower]Case(s))`
* `s == null => length(s) == 0`
* `s != null => length(s) > 0`

Stack:
=======
* `pop(push(s, x)) == x`
* `size(pop(push(x))) == size(push(x)) - 1 // size inherited from Vector`
* `size(push(push(x1), x2)) == size(push(x1)) + 1 // size inherited from Vector`
* `peek(push(x)) == x`
* `isEmpty(push(x)) == False`
* `s == null => size(s) == 0`
* `s != null => size(s) > 0`

HashMap:
=======
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
