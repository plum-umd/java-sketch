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

## Custom Codegen

To capture hole assignments, we will pass to Sketch
a custom code generator that will be invoked
at code generation time.
Pre-built `codegen.jar` is under `codegen/lib/`.

You can build it by yourself if you want to.
Make sure your environment is set up properly.
If you are using Sketch from source:
```
export SKETCH_HOME=/path/to/sketch-frontend
export PATH=$PATH:$SKETCH_HOME/target/sketch-1.6.9-noarch-launchers.dir
```
If you are using Sketch tar ball:
```
export SKETCH_HOME=/path/to/sketch-frontend/runtime
export PATH=$PATH:$SKETCH_HOME/..
```

Then,
```sh
$ cd codegen; ant
```
The build file (`build.xml`) assumes that Sketch is built
from source.  Otherwise, i.e., using a tar ball,
comment out lines 20--21 and 34, and uncomment lines 17--18 and 32.


[sk]: https://bitbucket.org/gatoatigrado/sketch-frontend/

