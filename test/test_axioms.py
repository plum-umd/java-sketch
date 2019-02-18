from __future__ import absolute_import
import os
import unittest

import java_sk.main
import java_sk.util
from . import TestCommon

pwd = os.path.dirname(__file__)
tests = os.path.join(pwd, "axioms/benchmarks")

class TestJava(TestCommon):
    def __test(self, fs, inline, unroll, adp_conc=False, arr=32):
        _fs = map(lambda f: os.path.join(tests, f), fs)
        if adp_conc:
            ret = java_sk.main.translate(prg=_fs, log_lvl='30', lib=False, opts=["--bnd-inline-amnt", str(inline), "--bnd-unroll-amnt", str(unroll), "--bnd-arr-size", str(arr), "--slv-timeout",  "10", "--slv-randassign", "--slv-simple-inputs"])
        else:
            ret = java_sk.main.translate(prg=_fs, log_lvl='30', lib=False, opts=["--bnd-inline-amnt", str(inline), "--bnd-unroll-amnt", str(unroll), "--bnd-arr-size", str(arr), "--slv-timeout",  "10"])
        self.assertEqual(ret, 0)

#################################################################
## MOCK TESTS
#################################################################

    def test_SuffixArrayRewrite(self):
        files = ["SuffixArray_loops2.java", "SuffixArrayTest.java", "rewrite/"]        
        files = map(lambda s: "SuffixArray_bigger/" + s, files)
        inline = 3
        unroll = 8
        self.__test(files, inline, unroll)        

    # def test_KafkaRewrite(self):
    #     # files = ["JCECipher_syn_rewrite.java", "OpenSSLCipher_syn_rewrite.java", "CipherFactory.java", "ICipher_rewrite.java", "Tester_rewrite.java", "rewrite/", "shared/"]
    #     files = ["JCECipher_syn.java", "OpenSSLCipher_syn.java", "CipherFactory.java", "ICipher_model.java", "Tester_model.java", "model/", "shared/"]
    #     files = map(lambda s: "Kafka_biggest/" + s, files)
    #     inline = 2
    #     unroll = 35
    #     # inline = 1
    #     # unroll = 15
    #     return self.__test(files, inline, unroll)        

    # def test_SimpleArrayListZ3(self):
    #     files = ["SimpleExample.java", "ArrayList.java", "Object.java"]
    #     files = map(lambda s: "SimpleArrayListExampleZ3/" + s, files)
    #     inline = 2
    #     unroll = 8
    #     self.__test(files, inline, unroll)
        
    # def test_RomList_bigger(self):
    #     files = ["RomlistParser_syn_model.java", "RomlistGame.java", "Tester.java", "model/", "shared/"]
    #     # files = ["RomlistParser_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "RomList_bigger/" + s, files)
    #     inline = 2
    #     unroll = 26
    #     # unroll = 19
    #     self.__test(files, inline, unroll, True)
    #     # self.__test(files, inline, unroll)

    # def test_ComparatorRewrite(self):
    #     files = ["CommunicationWithFiles_syn_rewrite.java", "Comparator_rewrite.java", "Tester.java", "rewrite/", "shared/"] 
    #     files = map(lambda s: "Comparator_bigger/" + s, files)
    #     inline = 2
    #     unroll = 10
    #     self.__test(files, inline, unroll, True)            

    # def test_PasswordManager_bigger(self):
    #     files = ["Cryptographer_syn_model.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "model/", "shared/"]
    #     # files = ["Cryptographer_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "PasswordManager_bigger/" + s, files)
    #     inline = 2
    #     unroll = 16
    #     self.__test(files, inline, unroll)
        
    # def test_EasyCSVRewrite_bigger(self):
    #     files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "EasyCSV_bigger/" + s, files)
    #     inline = 3
    #     unroll = 5
    #     # self.__test(files, inline, unroll, True)
    #     self.__test(files, inline, unroll)

    # def test_CipherFactoryModel_bigger(self):
    #     files = ["CryptoManager_syn_model.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_model.java", "ICipherFactory.java", "ICryptoManager.java", "model/", "shared/"]
    #     files = map(lambda s: "CipherFactory_bigger/" + s, files)
    #     inline = 2
    #     unroll = 9
    #     self.__test(files, inline, unroll)

    # def test_SuffixArrayModel_bigger(self):
    #     files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "model/"]        
    #     files = map(lambda s: "SuffixArray_bigger/" + s, files)
    #     inline = 3
    #     unroll = 8
    #     self.__test(files, inline, unroll)

    # def test_SuffixArrayModel(self):
    #     files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "model/"]        
    #     files = map(lambda s: "SuffixArray/" + s, files)
    #     inline = 2
    #     unroll = 8
    #     self.__test(files, inline, unroll)

    # def test_HashMap1Model(self):
    #     files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "model/", "shared/"]
    #     files = map(lambda s: "HashMap1/" + s, files)
    #     inline = 2
    #     unroll = 13
    #     self.__test(files, inline, unroll)
        
    # def test_HashMap2Model(self):
    #     files = ["Bucketing_syn.java", "BucketingTest.java", "HashTable.java", "Pair.java", "model/", "shared/"]
    #     files = map(lambda s: "HashMap2/" + s, files)
    #     inline = 1
    #     unroll = 11
    #     self.__test(files, inline, unroll)
        
    # def test_PasswordManagerModel(self):
    #     files = ["Cryptographer_syn_model.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "model/", "shared/"]
    #     files = map(lambda s: "PasswordManager/" + s, files)
    #     inline = 2
    #     unroll = 16
    #     self.__test(files, inline, unroll)
        
    # def test_CipherFactoryModel(self):
    #     files = ["CryptoManager_syn_model.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_model.java", "ICipherFactory.java", "ICryptoManager.java", "model/", "shared/"]
    #     files = map(lambda s: "CipherFactory/" + s, files)
    #     inline = 2
    #     unroll = 9
    #     self.__test(files, inline, unroll)
        
    # def test_KafkaModel(self):
    #     files = ["JCECipher_syn.java", "OpenSSLCipher_syn.java", "CipherFactory.java", "ICipher_model.java", "Tester.java", "model/", "shared/"]
    #     files = map(lambda s: "Kafka/" + s, files)
    #     inline = 2
    #     unroll = 35
    #     self.__test(files, inline, unroll)

    # def test_EasyCSVModel(self):
    #     files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "model/", "shared/"]
    #     files = map(lambda s: "EasyCSV/" + s, files)
    #     inline = 3
    #     unroll = 5
    #     self.__test(files, inline, unroll)

    # def test_RomListModel(self):
    #     files = ["RomlistParser_syn_model.java", "RomlistGame.java", "Tester.java", "model/", "shared/"]
    #     files = map(lambda s: "RomList/" + s, files)
    #     inline = 2
    #     unroll = 26
    #     self.__test(files, inline, unroll, True)

    # def test_ComparatorModel(self):
    #     files = ["CommunicationWithFiles_syn_model.java", "Comparator_model.java", "Tester.java", "model/", "shared/"]
    #     files = map(lambda s: "Comparator/" + s, files)
    #     inline = 2
    #     unroll = 10
    #     self.__test(files, inline, unroll, True, 50)

#################################################################
## REWRITE TESTS
#################################################################
    
    # def test_SuffixArrayRewrite(self):
    #     files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "rewrite/"]        
    #     files = map(lambda s: "SuffixArray/" + s, files)
    #     inline = 3
    #     unroll = 8
    #     self.__test(files, inline, unroll)        

    # def test_HashMap1Rewrite(self):
    #     files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "HashMap1/" + s, files)
    #     inline = 3
    #     unroll = 3
    #     self.__test(files, inline, unroll)

    # def test_HashMap2Rewrite(self):
    #     files = ["Bucketing_syn.java", "BucketingTest.java", "HashTable.java", "Pair.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "HashMap2/" + s, files)
    #     inline = 1
    #     unroll = 2
    #     self.__test(files, inline, unroll)

    # def test_PasswordManagerRewrite(self):
    #     files = ["Cryptographer_syn_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     # files = ["Cryptographer_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "PasswordManager/" + s, files)
    #     inline = 2
    #     unroll = 16
    #     self.__test(files, inline, unroll)
        
    # def test_PasswordManagerRewrite_nobox(self):
    #     files = ["Cryptographer_syn_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     # files = ["Cryptographer_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "PasswordManager_nobox/" + s, files)
    #     inline = 2
    #     unroll = 16
    #     self.__test(files, inline, unroll)
        
    # def test_CipherFactoryRewrite(self):
    #     files = ["CryptoManager_syn_rewrite.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_rewrite.java", "ICipherFactory.java", "ICryptoManager.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "CipherFactory/" + s, files)
    #     inline = 2
    #     unroll = 9
    #     self.__test(files, inline, unroll)

    # def test_CipherFactoryRewrite_nobox(self):
    #     files = ["CryptoManager_syn_rewrite.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_rewrite.java", "ICipherFactory.java", "ICryptoManager.java", "rewrite/", "shared/"]
    #     # files = ["CryptoManager_rewrite.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_rewrite.java", "ICipherFactory.java", "ICryptoManager.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "CipherFactory_nobox/" + s, files)
    #     inline = 2
    #     unroll = 9
    #     self.__test(files, inline, unroll)

    # def test_KafkaRewrite(self):
    #     files = ["JCECipher_syn_rewrite.java", "OpenSSLCipher_syn_rewrite.java", "CipherFactory.java", "ICipher_rewrite.java", "Tester.java", "rewrite/", "shared/"]
    #     # files = ["OpenSSLCipher_syn_rewrite", "JCECipher_syn_rewrite.java", "ICipher.java", "Tester.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "Kafka/" + s, files)
    #     inline = 2
    #     unroll = 35
    #     self.__test(files, inline, unroll)

    # def test_KafkaRewrite_nobox(self):
    #     files = ["JCECipher_syn_rewrite.java", "OpenSSLCipher_syn_rewrite.java", "CipherFactory.java", "ICipher_rewrite.java", "Tester.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "Kafka_nobox/" + s, files)
    #     inline = 2
    #     unroll = 35
    #     # inline = 1
    #     # unroll = 15
    #     self.__test(files, inline, unroll)

    # def test_EasyCSVRewrite(self):
    #     files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "EasyCSV/" + s, files)
    #     inline = 3
    #     unroll = 5
    #     # self.__test(files, inline, unroll, True)
    #     self.__test(files, inline, unroll)

    # def test_RomListRewrite(self):
    #     files = ["RomlistParser_syn_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
    #     # files = ["RomlistParser_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
    #     files = map(lambda s: "RomList/" + s, files)
    #     inline = 2
    #     unroll = 26
    #     # unroll = 19
    #     self.__test(files, inline, unroll, True)
    #     # self.__test(files, inline, unroll)

    # def test_ComparatorRewrite(self):
    #     files = ["CommunicationWithFiles_syn_rewrite.java", "Comparator_rewrite.java", "Tester.java", "rewrite/", "shared/"] 
    #     files = map(lambda s: "Comparator/" + s, files)
    #     inline = 2
    #     unroll = 10
    #     self.__test(files, inline, unroll, True)            


if __name__ == '__main__':
  unittest.main()
