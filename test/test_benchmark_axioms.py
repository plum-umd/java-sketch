from __future__ import absolute_import
from functools import reduce
import os
import unittest
import csv

import java_sk.main
import java_sk.util
import re
from . import TestCommon

pwd = os.path.dirname(__file__)
tests = os.path.join(pwd, "axioms/benchmarks")

numTests = 1

class TestJava(TestCommon):
    def __test(self, fs, inline, unroll, adp_conc=False, arr=32):
        _fs = [os.path.join(tests, f) for f in fs]
        if adp_conc:
            ret = java_sk.main.translate(prg=_fs, log_lvl='30', lib=False, opts=["--bnd-inline-amnt", str(inline), "--bnd-unroll-amnt", str(unroll), "--bnd-arr-size", str(arr), "--slv-timeout",  "10", "--slv-randassign", "--slv-simple-inputs"])
        else:
            ret = java_sk.main.translate(prg=_fs, log_lvl='30', lib=False, opts=["--bnd-inline-amnt", str(inline), "--bnd-unroll-amnt", str(unroll), "--bnd-arr-size", str(arr), "--slv-timeout",  "10"])
        # self.assertEqual(ret, 0)
        return ret
        
    def run_tests(self, tests, results):
        for k in range(0, len(tests)):
            (t, f) = tests[k]
            results.append([f])
            for i in range(0, numTests):
                result = 1
                while result != 0:
                    result = t()
                output = open('result/output/'+f+'.txt')
                text = [line for line in output][-1]
                time = re.match(r'Total time = ([0-9]*)', text, re.M|re.I)
                results[k].append(time.group(1))
                output.close()                
                # with open('result/output/'+f+'.txt') as output:
                #     text = [line for line in output][-1]
                #     time = re.match(r'Total time = ([0-9]*)', text, re.M|re.I)
                #     results[k].append(time.group(1))
            results[k].append('--'*8)
                    
        return results

    # def test_rand(self):
    #     for i in range(0, 31*200):
    #         output = open('result/output/'+str(i)+'.txt', 'w')
    #         output.write(str(i))
    #         output.close()
    #     for i in range(0, 31*200):
    #         output = open('result/output/'+str(i)+'.txt', 'r')
    #         text = [line for line in output][-1]
    #         time = re.match(r'Total time = ([0-9]*)', text, re.M|re.I)
    #         if time:
    #             print(time.group(1))
    #         # output.close()                
                
    def test_runModels(self):
        modelResults = open('results_model.csv', 'w')
        # with modelResults:
        writer = csv.writer(modelResults)
        modelTests = [
            (self.run_SuffixArrayModel, 'SuffixArrayTest'),
            (self.run_HashMap1Model, 'HashTableTest'),
            (self.run_HashMap2Model, 'BucketingTest'),
            (self.run_EasyCSVModel, 'CSVTester'),
            (self.run_RomListModel, 'RomListTester'),
            (self.run_ComparatorModel, 'Comparator'),
            (self.run_PasswordManagerModel, 'PasswordManagerTest'),
            (self.run_CipherFactoryModel, 'CipherFactoryTests'),
            (self.run_KafkaModel, 'Kafka_Tester')                
        ]
        results = [[x] for x in reduce(lambda x,y: x + y, self.run_tests(modelTests, []))]
        writer.writerows(results)
        modelResults.close()

    def test_runRewrites(self):
        modelResults = open('results_rewrite.csv', 'w')
        # with modelResults:
        writer = csv.writer(modelResults)
        rewriteTests = [
            (self.run_SuffixArrayRewrite, 'SuffixArrayTest'),
            (self.run_HashMap1Rewrite, 'HashTableTest'),
            (self.run_HashMap2Rewrite, 'BucketingTest'),
            (self.run_EasyCSVRewrite, 'CSVTester'),
            (self.run_RomListRewrite, 'RomListTester'),
            (self.run_ComparatorRewrite, 'Comparator'),
            (self.run_PasswordManagerRewrite, 'PasswordManagerTest'),
            (self.run_CipherFactoryRewrite, 'CipherFactoryTests'),
            (self.run_KafkaRewrite, 'Kafka_Tester')
        ]
        results = [[x] for x in reduce(lambda x,y: x + y, self.run_tests(rewriteTests, []))]
        writer.writerows(results)
        modelResults.close()
            
    def run_SuffixArrayModel(self):
        files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "model/"]        
        files = ["SuffixArray/" + s for s in files]
        inline = 2
        unroll = 8
        return self.__test(files, inline, unroll)
        
    def run_SuffixArrayRewrite(self):
        files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "rewrite/"]        
        files = ["SuffixArray/" + s for s in files]
        inline = 2
        unroll = 8
        return self.__test(files, inline, unroll)
        
    def run_HashMap1Model(self):
        files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "model/", "shared/"]
        files = ["HashMap1/" + s for s in files]
        inline = 3
        unroll = 13
        return self.__test(files, inline, unroll)
        
    def run_HashMap1Rewrite(self):
        files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "rewrite/", "shared/"]
        files = ["HashMap1/" + s for s in files]
        inline = 3
        unroll = 13
        return self.__test(files, inline, unroll)

    def run_HashMap2Model(self):
        files = ["Bucketing_syn.java", "BucketingTest.java", "HashTable.java", "Pair.java", "model/", "shared/"]
        files = ["HashMap2/" + s for s in files]
        inline = 1
        unroll = 11
        return self.__test(files, inline, unroll)
        
    def run_HashMap2Rewrite(self):
        files = ["Bucketing_syn.java", "BucketingTest.java", "HashTable.java", "Pair.java", "rewrite/", "shared/"]
        files = ["HashMap2/" + s for s in files]
        inline = 1
        unroll = 11 #2
        return self.__test(files, inline, unroll)

    def run_EasyCSVModel(self):
        files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "model/", "shared/"]
        files = ["EasyCSV/" + s for s in files]
        inline = 3
        unroll = 5
        return self.__test(files, inline, unroll)

    def run_EasyCSVRewrite(self):
        files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "rewrite/", "shared/"]
        files = ["EasyCSV/" + s for s in files]
        inline = 3
        unroll = 5
        # return self.__test(files, inline, unroll, True)
        return self.__test(files, inline, unroll)

    def run_RomListModel(self):
        files = ["RomlistParser_syn_model.java", "RomlistGame.java", "Tester.java", "model/", "shared/"]
        files = ["RomList/" + s for s in files]
        inline = 2
        unroll = 26
        return self.__test(files, inline, unroll, True)

    def run_RomListRewrite(self):
        files = ["RomlistParser_syn_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
        # files = ["RomlistParser_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
        files = ["RomList/" + s for s in files]
        inline = 2
        unroll = 26
        # unroll = 19
        return self.__test(files, inline, unroll, True)
        # return self.__test(files, inline, unroll)

    def run_ComparatorModel(self):
        files = ["CommunicationWithFiles_syn_model.java", "Comparator_model.java", "Tester.java", "model/", "shared/"]
        files = ["Comparator/" + s for s in files]
        inline = 2
        unroll = 10
        return self.__test(files, inline, unroll, True, 50)
        # return self.__test(files, inline, unroll, True)

    def run_ComparatorRewrite(self):
        files = ["CommunicationWithFiles_syn_rewrite.java", "Comparator_rewrite.java", "Tester.java", "rewrite/", "shared/"] 
        # files = ["CommunicationWithFiles_rewrite.java", "Comparator_rewrite.java", "Tester.java", "rewrite/", "shared/"] 
        files = ["Comparator/" + s for s in files]
        inline = 2 #2
        unroll = 10 #10
        return self.__test(files, inline, unroll, True)
        # return self.__test(files, inline, unroll)

    def run_PasswordManagerModel(self):
        files = ["Cryptographer_syn_model.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "model/", "shared/"]
        files = ["PasswordManager/" + s for s in files]
        inline = 2
        unroll = 16
        return self.__test(files, inline, unroll)
        
    def run_PasswordManagerRewrite(self):
        files = ["Cryptographer_syn_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
        # files = ["Cryptographer_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
        files = ["PasswordManager_nobox/" + s for s in files]
        inline = 2
        unroll = 16
        return self.__test(files, inline, unroll)
        
    def run_CipherFactoryModel(self):
        files = ["CryptoManager_syn_model.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_model.java", "ICipherFactory.java", "ICryptoManager.java", "model/", "shared/"]
        files = ["CipherFactory/" + s for s in files]
        inline = 2
        unroll = 9
        return self.__test(files, inline, unroll)
        
    def run_CipherFactoryRewrite(self):
        files = ["CryptoManager_syn_rewrite.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_rewrite.java", "ICipherFactory.java", "ICryptoManager.java", "rewrite/", "shared/"]
        # files = ["CryptoManager_rewrite.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_rewrite.java", "ICipherFactory.java", "ICryptoManager.java", "rewrite/", "shared/"]
        files = ["CipherFactory_nobox/" + s for s in files]
        inline = 2
        unroll = 9
        return self.__test(files, inline, unroll)

    def run_KafkaModel(self):
        files = ["JCECipher_syn.java", "OpenSSLCipher_syn.java", "CipherFactory.java", "ICipher_model.java", "Tester.java", "model/", "shared/"]
        files = ["Kafka/" + s for s in files]
        inline = 2
        unroll = 35
        return self.__test(files, inline, unroll)

    def run_KafkaRewrite(self):
        files = ["JCECipher_syn_rewrite.java", "OpenSSLCipher_syn_rewrite.java", "CipherFactory.java", "ICipher_rewrite.java", "Tester.java", "rewrite/", "shared/"]
        files = ["Kafka_nobox/" + s for s in files]
        inline = 2
        unroll = 35
        # inline = 1
        # unroll = 15
        return self.__test(files, inline, unroll)        

if __name__ == '__main__':
  unittest.main()
        
