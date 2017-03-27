***JSketch requires Java 8***

# JSketch

Sketch-based synthesis, epitomized by [Sketch][sk], lets developers
synthesize software starting from a _partial program_, also called a
_sketch_ or _template_.  JSketch is a tool that brings sketch-based
synthesis to Java. JSketch's input is a partial Java program that may
include _holes_, which are unknown constants, _expression generators_,
which range over sets of expressions, and _class generators_, which are
partial classes.  JSketch then translates the synthesis problem into
a [Sketch][sk] problem; this translation is complex becuase [Sketch][sk]
is not object-oriented.  Finally, JSketch synthesizes an executable Java
program by interpreting the output of [Sketch][sk].

## Requirement

Since this tool is a front-end for [Sketch][sk],
you need to install [Sketch][sk] and set up the environment.

* Tar ball

One way to build Sketch is to use an easy-to-install tar ball:
[sketch-1.7.0.tgz][sk-170].
Inside the tar ball, all Java files in sketch-frontend are already compiled,
so all you need to do is building sketch-backend.
Make sure that you have `gcc`, `g++`, `bison`, and `flex`.
(You may need to install `autoconf`, `automake`, and `libtool`, too.)
Then, build the beck-end as follows:
```sh
.../ $ tar xvfz sketch-1.7.0.tgz
.../ $ cd sketch-1.7.0/sketch-backend
.../sketch-1.7.0/sketch-backend $ chmod +x ./configure
.../sketch-1.7.0/sketch-backend $ ./configure
.../sketch-1.7.0/sketch-backend $ make clean; make
```
You can run a simple test case to make sure the build is correct:
```sh
.../ $ cd ../sketch-frontend
.../sketch-frontend $ ./sketch test/sk/seq/miniTest1.sk
```

* From source

In case you are interested, here is a harder way to build Sketch.
```sh
.../ $ hg clone https://bitbucket.org/gatoatigrado/sketch-frontend
.../ $ hg clone https://bitbucket.org/gatoatigrado/sketch-backend
```
Make sure that you have `java`, `javac`, and `mvn` for sketch-frontend;
`gcc`, `g++`, `bison`, and `flex` for sketch-backend.
(You may need to install `autoconf`, `automake`, and `libtool`, too.)
Then, build Sketch as follows:
```sh
.../ $ cd sketch-frontend
.../sketch-frontend $ make assemble-noarch
```
```sh
.../ $ cd sketch-backend
.../sketch-backend $ ./autogen.sh
.../sketch-backend $ chmod +x ./configure
.../sketch-backend $ ./configure
.../sketch-backend $ make clean; make
```

You can run a simple test case to make sure the build is correct:
```sh
.../ $ cd sketch-frontend
.../sketch-frontend $ make run-local-seq EXEC_ARGS="src/test/sk/seq/miniTest1.sk"
```

One possible issue you may encounter while building sketch-frontend is
the inconsistent Java version in Maven, e.g., Maven refers to Java 1.6
while the main Java you're using is 1.7 or higher.  In that case, set up
`$JAVA_HOME` properly.


* Environment setup

To use `sketch` from anywhere,
we recommend you to set up your environment accordingly.
For the tar ball users:
```sh
export SKETCH_HOME=/path/to/sketch-1.7.0/sketch-frontend/runtime
export PATH=$PATH:$SKETCH_HOME/..
```
For the source users:
```sh
export SKETCH_HOME=/path/to/sketch-frontend
export PATH=$PATH:$SKETCH_HOME/target/sketch-1.7.0-noarch-launchers
```

## Usage

To use this tool, you should generate the parser first,
which is explained just below.
(Parser and Lexer are automatically generated from a grammar file,
hence not maintained in the repository.)
You can skip custom codegen (and the regression test)
and move to script usages.

### Parser Generation
Currently working a non-master branch. To clone:
```sh
git clone
git checkout new-ast
```

### Parser Generation

We slightly changed Java grammar to support holes (written `??`),
generators in an expression-level (written {| e* |}) and
in a class-level (written `generator class ...`), as well as
a couple other syntactic sugars borrowed from [Sketch][sk],
such as `repeat` and `minrepeat`.
To read JSketch, again, you should generate our parser first:

```sh
cd parser
make
```

### Custom Codegen

To capture hole assignments, we will pass to Sketch
a custom code generator that will be invoked
at code generation time.  Under `codegen/lib/`,
pre-built `codegen.jar` is provided.

You can build it by yourself if you want to.
Again, make sure your environment is set up properly.
If you are using Sketch from source:
```
export SKETCH_HOME=/path/to/sketch-frontend
export PATH=$PATH:$SKETCH_HOME/target/sketch-1.7.0-noarch-launchers
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
comment out lines 20--21 and 34, and uncomment lines 17--18 and 32
(with modifying the version number if necessary).

#### jsk.sh

This is the main script that runs JSketch.
```sh
$ ./jsk.sh (input_file | input_dir)+ [options]*
```
For example,
```sh
$ ./jsk.sh test/new_ast/Construct.java
```

This will dump the files it creates into `result/sk_Construct/`.

#### sketch.py (This hasn't been changed in the new branch, but also hasn't been tested.)

This module is used to debug translated sketches;
we can maintain a snapshot of the translation process
and run a debug-loop: editing it manually, invoking Sketch, and
repeating this process again and again until we find stable sketches.
Based on manual edits, we can revise the translation process
in module `encoder`. 
```sh
$ python -m java_sk.sketch -p demo_name [option]*
$ ./java_sk/sketch.py -p demo_name [option]*
```

## Regression testing
To run regression tests:
```sh
$ python -m test.test_mini
$ python -m test.test_new_ast
```

## Limitations

As Java is a very large language, this tool currently only supports
a core subset of Java.  Unsupported features include:
packages, access control, exceptions, and concurrency.

Additionally, JSketch assumes the input sketch is type correct,
meaning the standard parts of the program are type correct, holes
are used either as integers or booleans, and expression generators
are type correct.

[sk]: https://bitbucket.org/gatoatigrado/sketch-frontend/
[sk-170]: http://people.csail.mit.edu/jsjeon/adaptive-concretization/sketch-1.7.0.tgz
