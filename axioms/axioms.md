String
======
* `length(concat(s1,s2)) == length(s1) + length(s2)`
* `length(replace(s1, c1, c2)) == length(s1)`
* `length(substring(s, i, j)) == j - i`
* `split(s1, s2).length <= length(s1) // inequality? are we ready for these?`
* `length(toUpper(s)) == length(s)`
* `toString(s) == s // boring…but maybe somehow a useful axiom`
* `compareToIgnoreCase(s) == compareTo(to[Upper|Lower]Case(s))`

Stack:
=======
* `pop(push(x)) == x`

HashMap:
=======
* `get(h, k) == get(clone(h), k)       // clone requires am explicit cast to HashMap...`
* `put(h, k, v) == put(clone(h), k, v)`
