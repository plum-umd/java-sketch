import os
from subprocess import call

from . import glob2

pwd = os.path.dirname(__file__)


# get the *sorted* list of file names in the designated path
# template/gui/awt -> [.../AWTEvent.java, .../BorderLayout.java, ...]
def get_files_from_path(path, ext):
    if os.path.isfile(path): return [path]
    else:  # i.e., folder
        files = glob2.glob(os.path.join(path, "**/*.{}".format(ext)))
        return sorted(files)  # to guarantee the order of files read

"""
handling javaparser AST
"""
def toAST(files, ext):
    prg_files = []
    for f in files:
        prg_files.extend(get_files_from_path(f, "java"))
    if not prg_files: exit('File(s) not found!')
    java_in = os.path.abspath(os.path.join(pwd, '../tests/ir_asts/API.java'))
    json_out = os.path.abspath(os.path.join(pwd, '../tests/ir_asts/java.json'))
    api = ""
    for fname in prg_files:
        with open(fname, 'r') as fd:
            api += fd.read()
    with open(java_in, 'w') as fd:
        fd.write(api)
    # this classpath stuff seems awful. Jsonify is hardcoded, passing a
    # single string to subprocess.call is platform dependant, and shell=True
    # can be a security vulnerability (if allowed to take user input).
    # This just got a whole lot nastier
    cmd = 'cd ' + pwd + '/..; /usr/bin/java -cp .:javaparser/javaparser-core/target/classes:$HOME/.m2/repository/com/cedarsoftware/json-io/4.3.0/json-io-4.3.0.jar parser.Jsonify ' + java_in + ' ' + json_out
    call(cmd, shell=True)
    return json_out
