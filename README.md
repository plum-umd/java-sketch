# Java Sketch

a Java front-end for [Sketch][sk], a program synthesis tool

## Parser Generation

We slightly changed Java grammar to support holes (`??`).
To read Java Sketch, generate our own parser first:
```sh
$ python -m grammar.gen
```
or
```sh
$ ./grammar/gen.py
```

[sk]: https://bitbucket.org/gatoatigrado/sketch-frontend/

