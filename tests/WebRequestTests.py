##
# File: WebRequestsTests.py
# Date:  07-Jan-2020  E. Peisach
#
# Updates:
##
"""Test cases for WebRequests
"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import unittest
import platform

from wwpdb.apps.editormodule.webapp.WebRequest import WebRequest, EditorInputRequest, ResponseContent


class MyWebRequest(WebRequest):
    """A class to provide access to methods for testing"""

    def getIntegerValue(self, myKey):
        return self._getIntegerValue(myKey)

    def getDoubleValue(self, myKey):
        return self._getDoubleValue(myKey)


class SessionTests(unittest.TestCase):
    def setUp(self):
        HERE = os.path.abspath(os.path.dirname(__file__))
        TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
        if not os.path.exists(TESTOUTPUT):  # pragma: no cover
            os.makedirs(TESTOUTPUT)
        self.__sessiontop = TESTOUTPUT
        sdir = os.path.join(self.__sessiontop, "sessions")
        if not os.path.exists(sdir):  # pragma: no cover
            os.makedirs(sdir)

    def testWebRequest(self):
        """Tests WebRequest access"""

        # No parameters
        wr = WebRequest()
        self.assertIn("WebRequest.printIt", str(wr))

        # With parameters to test code paths
        paramDict = {"TopSessionPath": [self.__sessiontop], "request_path": ["service/testpath"]}
        wr = WebRequest(paramDict)
        self.assertIn("WebRequest.printIt", str(wr))
        self.assertIn("WebRequest.printIt", repr(wr))
        wr.setValue("key1", "5")
        wr.setValueList("key2", ["6"])
        wr.printIt()
        self.assertIsInstance(wr.dump(format="html"), list)
        self.assertFalse(wr.exists("unknownkey"))
        js = wr.getJSON()
        wr.setJSON(js)
        self.assertEqual(wr.getValue("key1"), "5")
        # Empty spaces stripped
        wr.setValue("keyempty", " ")

        self.assertEqual(wr.getRawValue("key1"), "5")
        self.assertEqual(wr.getValueList("key1"), ["5"])

        mywr = MyWebRequest()
        mywr.setValue("key1", 5)
        mywr.setValue("key2", "5")
        mywr.setValue("key3", "2.5")
        self.assertEqual(mywr.getIntegerValue("key1"), 5)
        self.assertEqual(mywr.getIntegerValue("key2"), 5)
        self.assertEqual(mywr.getDoubleValue("key3"), 2.5)

    def testInputRequest(self):
        """Tests InputRequest access"""

        paramDict = {"TopSessionPath": [self.__sessiontop], "request_path": ["service/testpath"]}
        ir = EditorInputRequest(paramDict)
        # Test return format
        self.assertEqual(ir.getReturnFormat(), "")
        ir.setDefaultReturnFormat("html")
        ir.setReturnFormat("html")
        self.assertEqual(ir.getReturnFormat(), "html")
        self.assertEqual(ir.getRequestPath(), "service/testpath")
        sObj = ir.newSessionObj()
        self.assertNotEqual("", ir.getSessionId())
        self.assertIsNotNone(ir.getTopSessionPath())
        # No semaphore available in this interface
        self.assertEqual(ir.getSemaphore(), "")
        sid = sObj.getId()
        self.assertIsNotNone(sid)
        sObj = ir.getSessionObj()
        self.assertEqual(sid, sObj.getId())
        sObj = ir.newSessionObj()
        sid = sObj.getId()
        self.assertIsNotNone(sid)


class ResponseTests(unittest.TestCase):
    def setUp(self):
        HERE = os.path.abspath(os.path.dirname(__file__))
        TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
        if not os.path.exists(TESTOUTPUT):  # pragma: no cover
            os.makedirs(TESTOUTPUT)
        self.__sessiontop = TESTOUTPUT
        sdir = os.path.join(self.__sessiontop, "sessions")
        if not os.path.exists(sdir):  # pragma: no cover
            os.makedirs(sdir)
        self.__paramDict = {"TopSessionPath": [self.__sessiontop], "request_path": ["service/testpath"]}

    def testResponseConent(self):
        """Tests WebRequest access"""
        reqObj = EditorInputRequest(self.__paramDict)
        rc = ResponseContent(reqObj)

        # ResponseContent
        self.assertNotEqual(rc.get(), "")

        # Misc adds
        rc.setHtmlList(["<p>Hello</p>", "<p>There</p>"])
        rc.setHtmlText("Some text")
        reqObj.setReturnFormat("html")
        self.assertNotEqual(rc.get(), "")
        reqObj.setReturnFormat("text")
        self.assertNotEqual(rc.get(), "")
        reqObj.setReturnFormat("json")
        self.assertNotEqual(rc.get(), "")
        reqObj.setReturnFormat("jsonText")
        self.assertNotEqual(rc.get(), "")
        reqObj.setReturnFormat("jsonData")
        self.assertNotEqual(rc.get(), "")
        reqObj.setReturnFormat("location")
        self.assertNotEqual(rc.get(), "")
        reqObj.setReturnFormat("jsonp")
        self.assertNotEqual(rc.get(), "")
        reqObj.setReturnFormat("jsonText")
        self.assertNotEqual(rc.get(), "")

        # Error handling
        rc.setStatusCode("ok")

        # Files
        rc.setTextFile(__file__)
        rc.setHtmlContentPath("https://wwpdb.org")
        rc.get()

        self.assertIn("dump", rc.dump()[0])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
