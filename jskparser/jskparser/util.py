import os
from subprocess import call

from . import glob2

pwd = os.path.dirname(__file__)

def get_files_from_path(path, ext):
    # use set to remove duplicate files. weird...but it happens
    if os.path.isfile(path): return set([os.path.abspath(path)])
    else:  # i.e., folder
        files = glob2.glob(os.path.abspath(os.path.join(path, "**/*.{}".format(ext))))
        return set(sorted(files))  # to guarantee the order of files read

"""
handling javajskparser AST
"""
def toAST(files, ext, add_libs):
    prg_files = []
    for f in files:
        prg_files.extend(get_files_from_path(f, "java"))
    if not prg_files: exit('jskparser.util: File(s) not found!')
    java_in = os.path.abspath(os.path.join(pwd, '../tests/ir_asts/API.java'))
    json_out = os.path.abspath(os.path.join(pwd, '../tests/ir_asts/java.json'))
    if add_libs:
        obj_path = os.path.abspath(os.path.join(pwd, '../../model/lang/Object.java'))
        str_path = os.path.abspath(os.path.join(pwd, '../../model/lang/String.java'))
        num_path = os.path.abspath(os.path.join(pwd, '../../model/lang/Number.java'))
        int_path = os.path.abspath(os.path.join(pwd, '../../model/lang/Integer.java'))
        char_path = os.path.abspath(os.path.join(pwd, '../../model/lang/Character.java'))
        arr_path = os.path.abspath(os.path.join(pwd, '../../model/util/Arrays.java'))
        list_path = os.path.abspath(os.path.join(pwd, '../../model/util/List.java'))
        alist_path = os.path.abspath(os.path.join(pwd, '../../model/util/ArrayList.java'))
        llist_path = os.path.abspath(os.path.join(pwd, '../../model/util/LinkedList.java'))
        hmap_path = os.path.abspath(os.path.join(pwd, '../../model/util/HashMap.java'))
        if obj_path not in prg_files: prg_files.append(obj_path)
        if str_path not in prg_files: prg_files.append(str_path)
        if num_path not in prg_files: prg_files.append(num_path)
        if int_path not in prg_files: prg_files.append(int_path)
        if char_path not in prg_files: prg_files.append(char_path)
        if arr_path not in prg_files: prg_files.append(arr_path)
        if list_path not in prg_files: prg_files.append(list_path)
        if alist_path not in prg_files: prg_files.append(alist_path)
        if llist_path not in prg_files: prg_files.append(llist_path)
        if hmap_path not in prg_files: prg_files.append(hmap_path)
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
    cmd = 'cd ' + pwd + '/..; /usr/bin/java -cp .:javaparser/javaparser-core/target/classes:$HOME/.m2/repository/com/cedarsoftware/json-io/4.3.0/json-io-4.3.0.jar jskparser.Jsonify ' + java_in + ' ' + json_out
    ret = call(cmd, shell=True)
    if ret != 0: exit('Problem parsing.')
    return json_out
