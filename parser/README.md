## To clone:

	$ git clone git@gitlab.umiacs.umd.edu:plum/javaAST.git
	
	
## Compiling
**_This parser requires Java8_**. To build the parser:

It should be safe to just run `make` from the top level. To compile everything:

	$ make
	
For just the parser:

	$ make p
	
For just the json translator (this is used to convert parsed programs to a json representation):

	$ make j

## Parser Generation
The parser uses is a slight modification of
[JavaParser](http://javaparser.org/) with additions for syntactical
constructs we need and a dependency on the json library
[json-io](https://github.com/jdereg/json-io).

Installing JavaParser can take awhile and on some systems, as it has a lot of dependencies that need to be downloaded. If you have just installed Maven, you may need to make a .m2/repository directory.

## Running
There are several features available during parsing and can be used as follows:

	Usage: parser.py [options]* [FILE]+

	Options:
	-h, --help      show this help message and exit
    -r, --reach     whether or not to do reaching defs
	-f, --dataflow  whether or not to do dataflow analysis
	-i, --inputs    do input analysis
	-e E, --expr=E  start and stop nodes for i/o
	-d, --debug     print intermediate messages verbosely
	-v, --verbose   print dataflow results
	-s, --symtab    Print symbol tables

where `FILE` can be a list of Java programs or a directory. The parser will generate two files: `tests/ir_asts/API.java` and 
`tests/ir_asts/java.json` which contain a single Java file containing all the code passed in and a json representation of the AST, 
respectively. 

Examples: 

`./run.sh tests/ast/input/Creation.java` will parse `Creation.java`, generate the two files, and output the parsed file.

`./run.sh -frv tests/ast/input/Creation.java` will parse `Creation.java`, perform reaching definition analysis, and output the
AST with it's input and output sets filled in.

`./run.sh -fvi -e0 -e1 tests/dataflow/input/api0.java` will parse `Creation.java` and perform input/output analysis. This means
given statements 0-1 (inclusive), return the input types and output types. In this case, no inputs and `int` as output.
