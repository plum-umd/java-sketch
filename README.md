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
[sketch-1.7.6.tar][sk-176].
Inside the tar ball, all Java files in sketch-frontend are already compiled,
so all you need to do is building sketch-backend.
Make sure that you have `gcc`, `g++`, `bison`, and `flex`.
(You may need to install `autoconf`, `automake`, and `libtool`, too.)
Then, build the beck-end as follows:
```sh
.../ $ tar xvfz sketch-1.7.6.tgz
.../ $ cd sketch-1.7.6/sketch-backend
.../sketch-1.7.6/sketch-backend $ chmod +x ./configure
.../sketch-1.7.6/sketch-backend $ ./configure
.../sketch-1.7.6/sketch-backend $ make clean; make
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
export SKETCH_HOME=/path/to/sketch-1.7.6/sketch-frontend/runtime
export PATH=$PATH:$SKETCH_HOME/..
```
For the source users:
```sh
export SKETCH_HOME=/path/to/sketch-frontend
export PATH=$PATH:$SKETCH_HOME/target/sketch-1.7.6-noarch-launchers
```

## Usage

To use this tool, you should generate the parser first,
which is explained just below.
(Parser and Lexer are automatically generated from a grammar file,
hence not maintained in the repository.)
You can skip custom codegen (and the regression test)
and move to script usages.

### Parser Generation

We slightly changed Java grammar to support holes (written `??`),
generators in an expression-level (written {| e* |}) and
in a class-level (written `generator class ...`), as well as
a couple other syntactic sugars borrowed from [Sketch][sk],
such as `repeat` and `minrepeat`.
To read JSketch, again, you should generate our parser first:

```sh
cd jskparser
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
export PATH=$PATH:$SKETCH_HOME/target/sketch-1.7.6-noarch-launchers
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

## Java Code Generation

Java code generation (i.e. output of runnable Java code form the synthesis) was implemented in
an old version of JSketch, and was dropped later due to a rework in JSketch framework. Now it is
back-ported from the old framework.

To use Java code generation, the custom code generator must be compiled, you can use the pre-compiled
version as well.

Then you need to annotate the class you wish to output with `@JavaCodeGen`, so that the codegen would
add it to the output list:
```java
@JavaCodeGen
class TestCase {
    // method with holes
    public void testFunc() {
        int x = ??;
        // ...
    }
}
```

Next, when running, use `--java_codegen` to enable the generation:
```sh
$ ./jsk.sh --java_codegen [input files]
```
The generated Java code would be put in `result/java/`

Note that currently the Java code generator is not fully complete and thus unstable, enable it may cause
the synthesis to fail, since the codegen would need to rewrite the input code to allow easier hole extraction,
and the `rewrite` module is not supporting the full JSketch language yet, leading to undefined
behavior when these language features are present.

Unsupported language features include:

* Recursive generators
* Regex generators (e.g. `{| ( 0 | 1 ) |}`)

There might be other language features that may provoke undefined behavior, use this feature with care.
In general, benchmarks with non-recursive generators together with plain holes in them are most likely to
work without any issues, see `test/benchmarks/java-codegen.java` for an example.

This feature is currently under development, and may improve to support these features in the future.

## Regression testing
To run regression tests:
```sh
$ python -m test.test_mini
$ python -m test.test_new_ast
$ python -m test.test_java
$ python -m test.test_java_precisely
```
Two of the test\_java tests and one of the java\_precisely tests currently fail due to boxing/unboxing issues.

## Limitations

As Java is a very large language, this tool currently only supports
a core subset of Java.  Unsupported features include:
packages, access control, exceptions, and concurrency.

Additionally, JSketch assumes the input sketch is type correct,
meaning the standard parts of the program are type correct, holes
are used either as integers or booleans, and expression generators
are type correct.

[sk]: https://github.com/asolarlez/sketch-frontend
[sk-170]: http://people.csail.mit.edu/jsjeon/adaptive-concretization/sketch-1.7.0.tgz
[sk-176]: https://people.csail.mit.edu/asolar/sketch-1.7.6.tar.gz
