String
======
* `length(concat(s1,s2)) == length(s1) + length(s2)`
* `length(replace(s1, c1, c2)) == length(s1)`
* `length(substring(s, i, j)) == j - i`
* `split(s1, s2).length <= length(s1) // inequality? are we ready for these?`
* `length(toUpper(s)) == length(s)`
* `toString(s) == s // boring…but maybe somehow a useful axiom`
* `compareTo(f(s1), f(s2)) == compareToIgnoreCase(s1,s2) where f=to[Upper|Lower]Case(s))`
* `s == nil => length(s) == 0`
* `s != nil => length(s) > 0`

Stack:
=======
* `pop(push(x)) == x`
* `peek(push(x)) == x`
* `isEmpty(push(x)) == False`
* `search(push(x), x) == 1`
* `s == nil => size(s) == 0`
* `s != nil => size(s) > 0`

HashMap:
=======
* `get(put(h, k, v), k) == v`
* `get(clone(h), k == get(h, k)`
* `put(clone(h), k, v) == put(h, k, v)`
* `isEmpty(put(h, k, v)) == False`
* `remove(put(h, k, v), v) == nil`
* `remove(put(put(h, k1, v1), k2, v2), v2) == put(h, k1, v1)`
* `remove(put(put(h, k1, v1), k2, v2), v1) == put(h, k2, v2)`
* `get(remove(put(h, k, v), v), v) == nil`
* `get(remove(put(put(h, k1, v1), k2, v2), v1), v2) == v2`
* `containsKey(h, k) => put(h, k, v)`
* `containValue(h, v) => put(h, k, v)`
* `isEmpty(h) => size(h) == 0`
* `!isEmpty(h) => size(h) > 0`
* `h == nil => size(h) == 0`
* `h != nil => size(h) > 0`

ArrayList:
=========
* `add(clone(a), e) == add(a, e) // and other clone stuff`
* `isEmpty(add(a, e)) == False`
* `contains(add(a, e), e) == True`
* `get(add(a, e), 0) == e`
* `get(add(add(a, e1), e2), 1) == e2`
* `get(remove(add(a, e), e), e) == nil`
* `get(remove(add(add(a, e1), e2), e1), e2) == e2`
* `remove(add(a, v), v) == nil`
* `remove(a, put(put(a, k1, v1), k2, v2), v2) == put(a, k1, v1)`
* `remove(a, put(put(a, k1, v1), k2, v2), v1) == put(a, k2, v2)`
* `indexOf(add(a, e), e) == 0`
* `indexOf(add(add(a, e1), e2), e2) == 1`
* `size(sort(a)) == size(a)`
* `isEmpty(a) => size(a) == 0`
* `!isEmpty(a) => size(a) > 0`
* `a == nil => size(a) == 0`
* `a != nil => size(a) > 0`
