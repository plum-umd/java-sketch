# Java Sketch

a Java front-end for [Sketch][sk], a program synthesis tool


## Usage

To use this tool, you should first generate the parser,
which is explained just below.
You can skip custom codegen (and the regression test).


### Parser Generation

We slightly changed Java grammar to support holes (`??`)
and a couple other syntactic sugars borrowed from [Sketch][sk],
such as `repeat` and `minrepeat`.
To read Java Sketch, generate our own parser first:
```sh
$ python -m grammar.gen
```
or
```sh
$ ./grammar/gen.py
```


### Custom Codegen

To capture hole assignments, we will pass to Sketch
a custom code generator that will be invoked
at code generation time.  Under `codegen/lib/`,
pre-built `codegen.jar` is provided.

You can build it by yourself if you want to.
Make sure your environment is set up properly.
If you are using Sketch from source:
```
export SKETCH_HOME=/path/to/sketch-frontend
export PATH=$PATH:$SKETCH_HOME/target/sketch-1.6.9-noarch-launchers
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


### Test

This tool has three kinds of regression tests:
erroneous cases, mini benchmarks converted from [Sketch][sk],
and its own test cases that exercise Java features.
You can find test cases under `test/benchmarks/` folder
and run those regression tests as following:
```sh
$ python -m unittest -v test.test_erroneous
$ python -m unittest -v test.test_mini
$ python -m unittest -v test.test_java
```
or
```sh
$ python -m test.test_erroneous
$ python -m test.test_mini
$ python -m test.test_java
```

Note that `test_erroneous` has intentionally erroneous cases,
so do not be alarmed to see eye-catching error reports.
As long as the final report of the testing module is `OK`,
then it is indeed okay.

### Scripts

In addition to the main entrance of the tool (`main.py`),
we provide a couple useful scripts that can
retrieve basic information from the program (`program.py`)
or run intermediate sketch files (`sketch.py`).

#### main.py

```sh
$ python -m java_sk.main (input_file | input_dir)+ [option]*
```

#### meta/program.py

```sh
$ python -m java_sk.meta.program (input_file | input_dir)+ [option]*
```

#### sketch.py

```sh
$ python -m java_sk.sketch -p demo_name [option]*
$ ./java_sk/sketch.py -p demo_name [option]*
```


[sk]: https://bitbucket.org/gatoatigrado/sketch-frontend/

