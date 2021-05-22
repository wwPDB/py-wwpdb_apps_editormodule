#
# File:     doServiceRequestWebOb.wsgi
# Created:  26-Sep-2018
#
# Updated:
# 26-Sep-2018 EP    Ported fcgi version
"""
This top-level responder for requests to /services/.... url for the
wwPDB General Annotation editor application framework.

This version depends on WSGI

Adapted from mod_wsgi version -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import logging
import sys

from webob import Request, Response
from wwpdb.utils.config.ConfigInfo import getSiteId

#  - URL mapping and application specific classes are launched from EditorWebApp()
from wwpdb.apps.editormodule.webapp.EditorWebApp import EditorWebApp

# Create logger
FORMAT = '[%(levelname)s]-%(module)s.%(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class MyRequestApp(object):
    """  Handle server interaction using FCGI/WSGI and WebOb Request
         and Response objects.
    """

    def __init__(self, textString="doServiceRequest() - WebOb version", verbose=True, log=sys.stderr):
        """
        """
        self.__text = textString
        self.__verbose = verbose
        self.__lfh = log
        self.__siteId = None
        self._myParameterDict = {}

    def __dumpEnv(self, request):
        outL = []
        # outL.append('<pre align="left">')
        outL.append("\n------------------doServiceRequest()------------------------------\n")
        outL.append("Web server request data content:\n")
        outL.append("Text initialization:   %s\n" % self.__text)
        try:
            outL.append("Host:         %s\n" % request.host)
            outL.append("Path:         %s\n" % request.path)
            outL.append("Method:       %s\n" % request.method)
            outL.append("Query string: %s\n" % request.query_string)
            outL.append("Parameter List:\n")
            for name, value in request.params.items():
                outL.append("Request parameter:    %s:  %r\n" % (name, value))
        except:
            logger.exception("while dumping environment")

        outL.append("\n------------------------------------------------\n\n")
        # outL.append("</pre>")
        return outL

    def __call__(self, environment, responseApplication):
        """          WSGI callable entry point


        """
        myRequest = Request(environment)
        #
        self._myParameterDict = {}
        self.__siteId = getSiteId()
        try:
            if 'WWPDB_SITE_ID' in environment:
                self.__siteId = environment['WWPDB_SITE_ID']
                self.__lfh.write(
                    "+MyRequestApp.__call__() - WWPDB_SITE_ID environ variable captured as %s\n" % self.__siteId)
            '''
            for name,value in environment.items():
                self.__lfh.write("+MyRequestApp.__call__() - ENVIRON parameter:    %s:  %r\n" % (name,value))
            '''
            for name, value in myRequest.params.items():
                if name not in self._myParameterDict:
                    self._myParameterDict[name] = []
                self._myParameterDict[name].append(value)
                self.__lfh.write("+MyRequestApp.__call__() - REQUEST parameter:    %s:  %r\n" % (name, value))
            self._myParameterDict['request_path'] = [myRequest.path.lower()]
        except:
            logger.exception("while dumping environment")
            logger.error("contents of request data")
            logger.error("%s" % ("".join(self.__dumpEnv(request=myRequest))))
        ###
        ### At this point we have everything needed from the request !
        ###
        myResponse = Response()
        myResponse.status = '200 OK'
        myResponse.content_type = 'text/html'
        ###
        ###  Application specific functionality called here --
        ###  Application receives path and parameter info only!
        ###
        editormodule = EditorWebApp(parameterDict=self._myParameterDict, verbose=self.__verbose,
                                    log=self.__lfh, siteId=self.__siteId)
        rspD = editormodule.doOp()
        myResponse.content_type = rspD['CONTENT_TYPE']
        myResponse.body = rspD['RETURN_STRING']
        ####
        ###
        return myResponse(environment, responseApplication)


##
##  NOTE -  Verbose setting is set here ONLY!
##
application = MyRequestApp(textString="doServiceRequest() - WebOb version", verbose=True, log=sys.stderr)
#
