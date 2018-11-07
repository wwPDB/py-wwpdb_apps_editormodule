#!/usr/bin/env python

from wwpdb.apps.editormodule.io.PdbxMasterViewDictionary  import PdbxMasterViewDictionary

import unittest
import sys

class PdbxViewTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stderr
        self.__testConfig = 'resources/pdbx_display_view_info_master.cif'

        self.__dV = PdbxMasterViewDictionary(verbose = False)
        self.assertTrue(self.__dV.read(self.__testConfig))

    def tearDown(self):
        pass

    def testReadFiles(self):
        """Tests reading of the configuration file"""
        # Nothing as handled in setup...
        pass

    def testExpMethods(self):
        """Tests returned methods are correct"""
        meths = self.__dV.getMethods()
        meths.sort()

        self.assertEqual(['EC', 'EM', 'EM,NMR', 'NMR', 'X-RAY'], meths)

    def testViews(self):
        """Tests returned views are correct"""
        meths = self.__dV.getViews()
        meths.sort()

        self.assertEqual(['EC', 'EM', 'EM_NMR', 'EMmap', 'NMR', 'X-RAY'], meths)


    def testMethodsTrans(self):
        """Tests translation of experimental methods to internal"""
        
        tCases = [['X-RAY DIFFRACTION', 'X-RAY'],
                  ['SOLID-STATE NMR', 'NMR'],
                  ['SOLID-STATE NMR,SOLUTION NMR', 'NMR'],
                  ['SOLUTION NMR,SOLUTION SCATTERING', 'NMR'],
                  ['SOLUTION NMR,ELECTRON MICROSCOPY', 'EM,NMR']
                  ]
        for case in tCases:
            methods = case[0].split(',')
            expect = case[1]
            self.assertEqual(self.__dV.methodsToView(methods), expect)

    def testGenerateViews(self):
        """Tests can generate views"""
        meths = self.__dV.getMethods()
        meths.sort()

        for m in meths:
            cat = self.__dV.generateMethodsView(m)
            self.assertIsNotNone(cat)

    def testDefaultView(self):
        """Tests tdefault view for internal name"""
        
        tCases = [['X-RAY', 'AV1'],
                  ['NMR', 'NMR1'],
                  ['EM', 'EM1'],
                  ['EM,NMR', 'EM1'],
                  ['EC', 'EM1'],
                  ]
        for case in tCases:
            method = case[0]
            expect = case[1]
            self.assertEqual(self.__dV.getDefaultViewName(method), expect)


if __name__ == '__main__':
    # Run all tests -- 
    unittest.main()
    #
