import os
import unittest

import java_sk.main
import java_sk.util
from . import TestCommon

pwd = os.path.dirname(__file__)
tests = os.path.join(pwd, "axioms/benchmarks")

class TestJava(TestCommon):
    def __test(self, fs, inline, unroll):
        _fs = map(lambda f: os.path.join(tests, f), fs)
        ret = java_sk.main.translate(prg=_fs, log_lvl='30', lib=False, opts=["--bnd-inline-amnt", str(inline), "--bnd-unroll-amnt", str(unroll), "--slv-timeout 10"])
        self.assertEqual(ret, 0)

    # def test_SuffixArrayModel(self):
    #     files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "model/"]        
    #     files = map(lambda s: "SuffixArray/" + s, files)
    #     inline = 2
    #     unroll = 8
    #     self.__test(files, inline, unroll)

    # def test_SuffixArrayRewrite(self):
    #     files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "rewrite/"]        
    #     files = map(lambda s: "SuffixArray/" + s, files)
    #     inline = 2
    #     unroll = 8
    #     self.__test(files, inline, unroll)
        
    # def test_HashMap1Model(self):
    #     files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "model/"]
    #     files = map(lambda s: "HashMap1/" + s, files)
    #     inline = 2
    #     unroll = 13
    #     self.__test(files, inline, unroll)
        
    def test_HashMap1Rewrite(self):
        files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "rewrite/"]
        files = map(lambda s: "HashMap1/" + s, files)
        inline = 3
        unroll = 2
        self.__test(files, inline, unroll)
        

if __name__ == '__main__':
  unittest.main()
