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
* `empty(push(x)) == False`
* `search(push(x), x) == 1`
* `s == nil => size(s) == 0`
* `s != nil => size(s) > 0`

HashMap:
=======
* `get(put(h, k, v), k) == v // this is klunky syntax, but we want the get of a key to be 
  the value put with that key`
* `get(clone(h), k == get(h, k)      // clone requires am explicit cast to HashMap...`
* `put(clone(h), k, v) == put(h, k, v)`
* `remove(h, put(h, k, v), v) == nil`
* `remove(h, put(h, put(h, v1), v2), v2) == put(h, v1)`
* `remove(h, put(h, put(h, v1), v2), v1) == put(h, v2)`
* `get(h, remove(h, put(h, x), x), x) == nil`
* `get(h, remove(h, put(h, put(h, x), y), x), y) == y`
* `containsKey(h, k) => put(h, k, v)`
* `containValue(h, v) => put(h, k, v)`
* `h == nil => size(h) == 0`
* `h != nil => size(h) > 0`

ArrayList:
=========
* `size(sort(a)) == size(a)`
* `a == nil => size(a) == 0`
* `a != nil => size(a) > 0`
