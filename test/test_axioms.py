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
        _fs = [os.path.join(tests, f) for f in fs]
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
        files = ["SuffixArray_bigger/" + s for s in files]
        inline = 3
        unroll = 8
        self.__test(files, inline, unroll)        

    # def test_KafkaRewrite(self):
    #     # files = ["JCECipher_syn_rewrite.java", "OpenSSLCipher_syn_rewrite.java", "CipherFactory.java", "ICipher_rewrite.java", "Tester_rewrite.java", "rewrite/", "shared/"]
    #     files = ["JCECipher_syn.java", "OpenSSLCipher_syn.java", "CipherFactory.java", "ICipher_model.java", "Tester_model.java", "model/", "shared/"]
    #     files = ["Kafka_biggest/" + s for s in files]
    #     inline = 2
    #     unroll = 35
    #     # inline = 1
    #     # unroll = 15
    #     return self.__test(files, inline, unroll)        

    # def test_SimpleArrayListZ3(self):
    #     files = ["SimpleExample.java", "ArrayList.java", "Object.java"]
    #     files = ["SimpleArrayListExampleZ3/" + s for s in files]
    #     inline = 2
    #     unroll = 8
    #     self.__test(files, inline, unroll)

    # def test_RomList_bigger(self):
    #     files = ["RomlistParser_syn_model.java", "RomlistGame.java", "Tester.java", "model/", "shared/"]
    #     # files = ["RomlistParser_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
    #     files = ["RomList_bigger/" + s for s in files]
    #     inline = 2
    #     unroll = 26
    #     # unroll = 19
    #     self.__test(files, inline, unroll, True)
    #     # self.__test(files, inline, unroll)

    # def test_ComparatorRewrite(self):
    #     files = ["CommunicationWithFiles_syn_rewrite.java", "Comparator_rewrite.java", "Tester.java", "rewrite/", "shared/"] 
    #     files = ["Comparator_bigger/" + s for s in files]
    #     inline = 2
    #     unroll = 10
    #     self.__test(files, inline, unroll, True)            

    # def test_PasswordManager_bigger(self):
    #     files = ["Cryptographer_syn_model.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "model/", "shared/"]
    #     # files = ["Cryptographer_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     files = ["PasswordManager_bigger/" + s for s in files]
    #     inline = 2
    #     unroll = 16
    #     self.__test(files, inline, unroll)

    # def test_EasyCSVRewrite_bigger(self):
    #     files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "rewrite/", "shared/"]
    #     files = ["EasyCSV_bigger/" + s for s in files]
    #     inline = 3
    #     unroll = 5
    #     # self.__test(files, inline, unroll, True)
    #     self.__test(files, inline, unroll)

    # def test_CipherFactoryModel_bigger(self):
    #     files = ["CryptoManager_syn_model.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_model.java", "ICipherFactory.java", "ICryptoManager.java", "model/", "shared/"]
    #     files = ["CipherFactory_bigger/" + s for s in files]
    #     inline = 2
    #     unroll = 9
    #     self.__test(files, inline, unroll)

    # def test_SuffixArrayModel_bigger(self):
    #     files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "model/"]        
    #     files = ["SuffixArray_bigger/" + s for s in files]
    #     inline = 3
    #     unroll = 8
    #     self.__test(files, inline, unroll)

    # def test_SuffixArrayModel(self):
    #     files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "model/"]        
    #     files = ["SuffixArray/" + s for s in files]
    #     inline = 2
    #     unroll = 8
    #     self.__test(files, inline, unroll)

    # def test_HashMap1Model(self):
    #     files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "model/", "shared/"]
    #     files = ["HashMap1/" + s for s in files]
    #     inline = 2
    #     unroll = 13
    #     self.__test(files, inline, unroll)

    # def test_HashMap2Model(self):
    #     files = ["Bucketing_syn.java", "BucketingTest.java", "HashTable.java", "Pair.java", "model/", "shared/"]
    #     files = ["HashMap2/" + s for s in files]
    #     inline = 1
    #     unroll = 11
    #     self.__test(files, inline, unroll)

    # def test_PasswordManagerModel(self):
    #     files = ["Cryptographer_syn_model.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "model/", "shared/"]
    #     files = ["PasswordManager/" + s for s in files]
    #     inline = 2
    #     unroll = 16
    #     self.__test(files, inline, unroll)

    # def test_CipherFactoryModel(self):
    #     files = ["CryptoManager_syn_model.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_model.java", "ICipherFactory.java", "ICryptoManager.java", "model/", "shared/"]
    #     files = ["CipherFactory/" + s for s in files]
    #     inline = 2
    #     unroll = 9
    #     self.__test(files, inline, unroll)

    # def test_KafkaModel(self):
    #     files = ["JCECipher_syn.java", "OpenSSLCipher_syn.java", "CipherFactory.java", "ICipher_model.java", "Tester.java", "model/", "shared/"]
    #     files = ["Kafka/" + s for s in files]
    #     inline = 2
    #     unroll = 35
    #     self.__test(files, inline, unroll)

    # def test_EasyCSVModel(self):
    #     files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "model/", "shared/"]
    #     files = ["EasyCSV/" + s for s in files]
    #     inline = 3
    #     unroll = 5
    #     self.__test(files, inline, unroll)

    # def test_RomListModel(self):
    #     files = ["RomlistParser_syn_model.java", "RomlistGame.java", "Tester.java", "model/", "shared/"]
    #     files = ["RomList/" + s for s in files]
    #     inline = 2
    #     unroll = 26
    #     self.__test(files, inline, unroll, True)

    # def test_ComparatorModel(self):
    #     files = ["CommunicationWithFiles_syn_model.java", "Comparator_model.java", "Tester.java", "model/", "shared/"]
    #     files = ["Comparator/" + s for s in files]
    #     inline = 2
    #     unroll = 10
    #     self.__test(files, inline, unroll, True, 50)

#################################################################
## REWRITE TESTS
#################################################################

    # def test_SuffixArrayRewrite(self):
    #     files = ["SuffixArray_loops.java", "SuffixArrayTest.java", "rewrite/"]        
    #     files = ["SuffixArray/" + s for s in files]
    #     inline = 3
    #     unroll = 8
    #     self.__test(files, inline, unroll)        

    # def test_HashMap1Rewrite(self):
    #     files = ["HashTable_loops.java", "HashTableNode.java", "HashTableTest.java", "rewrite/", "shared/"]
    #     files = ["HashMap1/" + s for s in files]
    #     inline = 3
    #     unroll = 3
    #     self.__test(files, inline, unroll)

    # def test_HashMap2Rewrite(self):
    #     files = ["Bucketing_syn.java", "BucketingTest.java", "HashTable.java", "Pair.java", "rewrite/", "shared/"]
    #     files = ["HashMap2/" + s for s in files]
    #     inline = 1
    #     unroll = 2
    #     self.__test(files, inline, unroll)

    # def test_PasswordManagerRewrite(self):
    #     files = ["Cryptographer_syn_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     # files = ["Cryptographer_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     files = ["PasswordManager/" + s for s in files]
    #     inline = 2
    #     unroll = 16
    #     self.__test(files, inline, unroll)

    # def test_PasswordManagerRewrite_nobox(self):
    #     files = ["Cryptographer_syn_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     # files = ["Cryptographer_rewrite.java", "PasswordManager_syn.java", "PasswordMap.java", "PasswordManagerTest.java", "rewrite/", "shared/"]
    #     files = ["PasswordManager_nobox/" + s for s in files]
    #     inline = 2
    #     unroll = 16
    #     self.__test(files, inline, unroll)

    # def test_CipherFactoryRewrite(self):
    #     files = ["CryptoManager_syn_rewrite.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_rewrite.java", "ICipherFactory.java", "ICryptoManager.java", "rewrite/", "shared/"]
    #     files = ["CipherFactory/" + s for s in files]
    #     inline = 2
    #     unroll = 9
    #     self.__test(files, inline, unroll)

    # def test_CipherFactoryRewrite_nobox(self):
    #     files = ["CryptoManager_syn_rewrite.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_rewrite.java", "ICipherFactory.java", "ICryptoManager.java", "rewrite/", "shared/"]
    #     # files = ["CryptoManager_rewrite.java", "CipherFactoryTester.java", "ConfigurableCipherFactory.java", "DefaultCipherFactory_rewrite.java", "ICipherFactory.java", "ICryptoManager.java", "rewrite/", "shared/"]
    #     files = ["CipherFactory_nobox/" + s for s in files]
    #     inline = 2
    #     unroll = 9
    #     self.__test(files, inline, unroll)

    # def test_KafkaRewrite(self):
    #     files = ["JCECipher_syn_rewrite.java", "OpenSSLCipher_syn_rewrite.java", "CipherFactory.java", "ICipher_rewrite.java", "Tester.java", "rewrite/", "shared/"]
    #     # files = ["OpenSSLCipher_syn_rewrite", "JCECipher_syn_rewrite.java", "ICipher.java", "Tester.java", "rewrite/", "shared/"]
    #     files = ["Kafka/" + s for s in files]
    #     inline = 2
    #     unroll = 35
    #     self.__test(files, inline, unroll)

    # def test_KafkaRewrite_nobox(self):
    #     files = ["JCECipher_syn_rewrite.java", "OpenSSLCipher_syn_rewrite.java", "CipherFactory.java", "ICipher_rewrite.java", "Tester.java", "rewrite/", "shared/"]
    #     files = ["Kafka_nobox/" + s for s in files]
    #     inline = 2
    #     unroll = 35
    #     # inline = 1
    #     # unroll = 15
    #     self.__test(files, inline, unroll)

    # def test_EasyCSVRewrite(self):
    #     files = ["CsvDocument_syn.java", "CodeAssertion.java", "CsvColumn.java", "CsvColumnTest.java", "CsvConfiguration.java", "CsvDocumentTest.java", "CsvRow.java", "CsvRowTest.java", "Tester.java", "rewrite/", "shared/"]
    #     files = ["EasyCSV/" + s for s in files]
    #     inline = 3
    #     unroll = 5
    #     # self.__test(files, inline, unroll, True)
    #     self.__test(files, inline, unroll)

    # def test_RomListRewrite(self):
    #     files = ["RomlistParser_syn_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
    #     # files = ["RomlistParser_rewrite.java", "RomlistGame.java", "Tester.java", "rewrite/", "shared/"]
    #     files = ["RomList/" + s for s in files]
    #     inline = 2
    #     unroll = 26
    #     # unroll = 19
    #     self.__test(files, inline, unroll, True)
    #     # self.__test(files, inline, unroll)

    # def test_ComparatorRewrite(self):
    #     files = ["CommunicationWithFiles_syn_rewrite.java", "Comparator_rewrite.java", "Tester.java", "rewrite/", "shared/"] 
    #     files = ["Comparator/" + s for s in files]
    #     inline = 2
    #     unroll = 10
    #     self.__test(files, inline, unroll, True)            


if __name__ == '__main__':
  unittest.main()
