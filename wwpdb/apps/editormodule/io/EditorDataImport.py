##
# File:    EditorDataImport.py
# Date:    21-Sep-2010
#
# Update:
#
# 2012-02-02    RPS    Ported here from ChemCompDataImport
# 2012-09-25    RPS    Now obtaining pdbx model file from WF archival storage as opposed to instance storage.
##

"""
Class to encapsulate data import for files requested by General Annotation Editor from the workflow directory hierarchy.

"""
__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "jwest@rcsb.rutgers.edu"
__license__   = "Creative Commons Attribution 3.0 Unported"
__version__   = "V0.01"


import sys, os, os.path, traceback, time

from wwpdb.api.facade.DataReference  import DataFileReference

class EditorDataImport(object):
    """ Controlling class for data import operations

        Supported file sources:
        + archive         -  WF archive storage  
        + wf-instance     -  WF instance storage 
        
    """
    def __init__(self,reqObj=None,verbose=False,log=sys.stderr):
        self.__verbose=verbose
        self.__reqObj=reqObj
        self.__lfh=log
        #
        self.__sessionObj = None
        #
        if (self.__verbose):
            self.__lfh.write("+EditorDataImport() starting\n")
            self.__lfh.flush()
        #
        self.__setup()
        #

    def __setup(self):
        
        try:
            self.__sessionObj  = self.__reqObj.getSessionObj()
            self.__sessionPath = self.__sessionObj.getPath()
            self.__identifier  = str(self.__reqObj.getValue("identifier")).upper()
            self.__instance    = str(self.__reqObj.getValue("instance")).upper()
            self.__fileSource = "archive" # 2012-09-25, decision made to always source model file from archival storage instead of instance (may need to revisit)
            '''
            self.__fileSource  = str(self.__reqObj.getValue("filesource")).lower()
            if self.__fileSource not in ['archive','wf-archive','wf-instance','wf_archive','wf_instance']:
                self.__fileSource = 'archive'            
            '''
            if (self.__verbose):
                self.__lfh.write("+EditorDataImport.__setup() file source %s\n" % self.__fileSource)
                self.__lfh.write("+EditorDataImport.__setup() identifier  %s\n" % self.__identifier)
                self.__lfh.write("+EditorDataImport.__setup() instance    %s\n" % self.__instance)
                #
                self.__lfh.flush()                
        except:
            if (self.__verbose):
                self.__lfh.write("+EditorDataImport.__setup() sessionId %s failed\n" % self.__sessionObj.getId())

    def getModelPdxFilePath(self):
        return self.__getWfFilePath(contentType='model',format='pdbx',fileSource=self.__fileSource,version='latest')

    def __getWfFilePath(self,contentType='model',format='pdbx',fileSource='archive',version='latest'):
        try:
            fPath=self.__getWfFilePathRef(contentType=contentType,format=format,fileSource=fileSource,version=version)
            if (self.__verbose):
                self.__lfh.write("+EditorDataImport.__getWfFilePath() checking %s  path %s\n" % (contentType,fPath))            
            if fPath is not None and os.access(fPath,os.R_OK):
                return fPath
            else:
                return None
        except:
            if (self.__verbose):
                traceback.print_exc(file=self.__lfh)
                self.__lfh.flush()                                        
            return None
        
    def __getWfFilePathRef(self,contentType='model',format='pdbx',fileSource='archive',version='latest'):
        """ Return the path to the latest version of the 
        """                
        #
        # Get PDBx model file -
        #
        dfRef=DataFileReference()
        self.__lfh.write("+EditorDataImport.__getWfFilePath() site id is %s\n" % dfRef.getSitePrefix())        

        dfRef.setDepositionDataSetId(self.__identifier)        
        if (fileSource in ['archive','wf-archive','wf_archive']):
            dfRef.setStorageType('archive')
        elif (fileSource in ['wf-instance','wf_instance']):
            dfRef.setWorkflowInstanceId(self.__instance)            
            dfRef.setStorageType('wf-instance')
        else:
            self.__lfh.write("+EditorDataImport.__getWfFilePath() Bad file source for %s id %s wf id %s\n" %
                             (contentType,self.__identifier,self.__instance))
        #
        dfRef.setContentTypeAndFormat(contentType,format)
        dfRef.setVersionId(version)        
        #
        fP=None
        if (dfRef.isReferenceValid()):                  
            dP=dfRef.getDirPathReference()
            fP=dfRef.getFilePathReference()
            if (self.__verbose):                
                self.__lfh.write("+EditorDataImport.__getWfFilePath() file directory path: %s\n" % dP)
                self.__lfh.write("+EditorDataImport.__getWfFilePath() file           path: %s\n" % fP)
        else:
            self.__lfh.write("+EditorDataImport.__getWfFilePath() bad reference for %s id %s wf id %s\n" %
                             (contentType,self.__identifier,self.__instance))                                
        
        self.__lfh.flush()        
        #
        return fP


if __name__ == '__main__':
    di=EditorDataImport()
