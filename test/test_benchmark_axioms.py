import os
import unittest
import csv

import java_sk.main
import java_sk.util
import re
from . import TestCommon

pwd = os.path.dirname(__file__)
tests = os.path.join(pwd, "axioms/benchmarks")

numTests = 5

class TestJava(TestCommon):
    def __test(self, fs, inline, unroll, adp_conc=False, arr=32):
        _fs = map(lambda f: os.path.join(tests, f), fs)
        if adp_conc:
            ret = java_sk.main.translate(prg=_fs, log_lvl='30', lib=False, opts=["--bnd-inline-amnt", str(inline), "--bnd-unroll-amnt", str(unroll), "--bnd-arr-size", str(arr), "--slv-timeout",  "10", "--slv-randassign", "--slv-simple-inputs"])
        else:
            ret = java_sk.main.translate(prg=_fs, log_lvl='30', lib=False, opts=["--bnd-inline-amnt", str(inline), "--bnd-unroll-amnt", str(unroll), "--bnd-arr-size", str(arr), "--slv-timeout",  "10"])
        self.assertEqual(ret, 0)

    def run_tests(self, tests, results):
        for k in range(0, len(tests)):
            (t, f) = tests[k]
            results.append([f])
            for i in range(0, numTests):
                t()
                with open('result/output/'+f+'.txt') as output:
                    text = [line for line in output][-1]
                    time = re.match(r'Total time = ([0-9]*)', text, re.M|re.I)
                    results[k].append(time.group(1))
            results[k].append('--'*8)
                    
        return results
        
    def test_runModels(self):
        modelResults = open('results_model.csv', 'w')
        with modelResults:
            writer = csv.writer(modelResults)
            modelTests = [
                (self.run_SuffixArrayModel, 'SuffixArrayTest'),
                (self.run_HashMap1Model, 'HashTableTest'),
                (self.run_HashMap2Model, 'BucketingTest'),
                (self.run_EasyCSVModel, 'CSVTester'),
                (self.run_RomListModel, 'RomListTester'),
                (self.run_ComparatorModel, 'Comparator')
            ]
            results = map(lambda x: [x], reduce(lambda x,y: x + y, self.run_tests(modelTests, [])))
            writer.writerows(results)

    def test_runRewrites(self):
        modelResults = open('results_rewrite.csv', 'w')
        with modelResults:
            writer = csv.writer(modelResults)
            rewriteTests = [
                (self.run_SuffixArrayRewrite, 'SuffixArrayTest'),
                (self.run_HashMap1Rewrite, 'HashTableTest'),
                (self.run_HashMap2Rewrite, 'BucketingTest'),
                (self.run_EasyCSVRewrite, 'CSVTester'),
                (self.run_RomListRewrite, 'RomListTester'),
                (self.run_ComparatorRewrite, 'Comparator')
            ]
            results = map(lambda x: [x], reduce(lambda x,y: x + y, self.run_tests(rewriteTests, [])))
            writer.writerows(results)
            
    def run_SuffixArrayModel(self):
        files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "model/"]        
        files = map(lambda s: "SuffixArray/" + s, files)
        inline = 2
        unroll = 8
        self.__test(files, inline, unroll)
        
    def run_SuffixArrayRewrite(self):
        files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "rewrite/"]        
        files = map(lambda s: "SuffixArray/" + s, files)
        inline = 2
        unroll = 8
        self.__test(files, inline, unroll)
        
    def run_HashMap1Model(self):
        files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "model/", "shared/"]
        files = map(lambda s: "HashMap1/" + s, files)
        inline = 2
        unroll = 13
        self.__test(files, inline, unroll)
        
    def run_HashMap1Rewrite(self):
        files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "rewrite/", "shared/"]
        files = map(lambda s: "HashMap1/" + s, files)
        inline = 3
        unroll = 3
        self.__test(files, inline, unroll)

    def run_HashMap2Model(self):
        files = ["Bucketing_syn.java", "BucketingTest.java", "HashTable.java", "Pair.java", "model/", "shared/"]
        files = map(lambda s: "HashMap2/" + s, files)
        inline = 1
        unroll = 11
        self.__test(files, inline, unroll)
        
    def run_HashMap2Rewrite(self):
        files = ["Bucketing_syn.java", "BucketingTest.java", "HashTable.java", "Pair.java", "rewrite/", "shared/"]
        files = map(lambda s: "HashMap2/" + s, files)
        inline = 1
        unroll = 2
        self.__test(files, inline, unroll)

    def run_EasyCSVModel(self):
        files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "model/", "shared/"]
        files = map(lambda s: "EasyCSV/" + s, files)
        inline = 3
        unroll = 5
        self.__test(files, inline, unroll)

    def run_EasyCSVRewrite(self):
        files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "rewrite/", "shared/"]
        files = map(lambda s: "EasyCSV/" + s, files)
        inline = 3
        unroll = 5
        # self.__test(files, inline, unroll, True)
        self.__test(files, inline, unroll)

    def run_RomListModel(self):
        files = ["RomlistParser_syn_model.java", "RomlistGame.java", "Tester.java", "model/", "shared/"]
        files = map(lambda s: "RomList/" + s, files)
        inline = 2
        unroll = 26
        self.__test(files, inline, unroll, True)

    def run_RomListRewrite(self):
        files = ["RomlistParser_syn_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
        # files = ["RomlistParser_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
        files = map(lambda s: "RomList/" + s, files)
        inline = 2
        unroll = 26
        # unroll = 19
        self.__test(files, inline, unroll, True)
        # self.__test(files, inline, unroll)

    def run_ComparatorModel(self):
        files = ["CommunicationWithFiles_syn_model.java", "Comparator_model.java", "Tester.java", "model/", "shared/"]
        files = map(lambda s: "Comparator/" + s, files)
        inline = 2
        unroll = 10
        self.__test(files, inline, unroll, True, 50)
        # self.__test(files, inline, unroll, True)

    def run_ComparatorRewrite(self):
        files = ["CommunicationWithFiles_syn_rewrite.java", "Comparator_rewrite.java", "Tester.java", "rewrite/", "shared/"] 
        # files = ["CommunicationWithFiles_rewrite.java", "Comparator_rewrite.java", "Tester.java", "rewrite/", "shared/"] 
        files = map(lambda s: "Comparator/" + s, files)
        inline = 2 #2
        unroll = 10 #10
        self.__test(files, inline, unroll, True)
        # self.__test(files, inline, unroll)

if __name__ == '__main__':
  unittest.main()
        
