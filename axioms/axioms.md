String
======
* `length(concat(s1,s2)) == length(s1) + length(s2)`
* `length(replace(s1, c1, c2)) == length(s1)`
* `length(substring(s, i, j)) == j - i`
* `split(s1, s2).length <= length(s1) // inequality? are we ready for these?`
* `length(toUpper(s)) == length(s)`
* `toString(s) == s // boring…but maybe somehow a useful axiom`
* `compareTo(f(s1), f(s2)) == compareToIgnoreCase(s1,s2) where f=to[Upper|Lower]Case(s))`

Stack:
=======
* `pop(push(x)) == x`
* `peek(push(x)) == x`
* `empty(push(x)) == False`
* `search(push(x), x) == 1`

HashMap:
=======
* `get(put(h, k, v), k) == v // this is klunky syntax, but we want the get of a key to be 
  the value put with that key`
* `get(clone(h), k == get(h, k)      // clone requires am explicit cast to HashMap...`
* `put(clone(h), k, v) == put(h, k, v)`

ArrayList:
=========
* `size(sort(a)) == size(a)`
* 
