# -*- coding: utf-8 -*-
# Copyright 2006 St James Software

"""Tests for the IterativeTester framework. Also serves as a usage example.
   Framework is used as follows:
     * Create or import some Dimension classes (Dimensions for common resources
       like databases, webservers, etc should be provided as part of the testing
       framework)
     * Subclass IterativeTester and populate the class attribute DIMENSIONS with
       information about what prefixes you're using for tests which need to be
       iterated over and the Dimensions which supply their arguments.
"""

from IterativeTester import IterativeTester, Dimension

#
# Dimensions
#

class WebServer_Dim1(Dimension):
    def __init__(self):
        self._resources = { 'webA' : 1, 'webB' : 2 }

class Databases_Dim2(Dimension):
    def __init__(self):
        self._resources = { 'dbA' : 3, 'dbB' : 4 }

#
# The tests
#

class TestExample(IterativeTester):
    DIMENSIONS = { 'webdb_test' : [WebServer_Dim1(), Databases_Dim2()],
                   'dbonly_test' : [Databases_Dim2()] }
    
    def webdb_test_A(self,webserver,db):
        print "A", webserver, db
    
    def webdb_test_B(self,webserver,db):
        print "B", webserver, db
   
    def dbonly_test_C(self,db):
        print "C", db
        assert db == 3  
   
    @classmethod 
    def setup_class_webdb_test(cls,webserver,db):
        print "Setup", webserver, db
    
    @classmethod
    def testSomeOtherThing(cls):
        assert True
    
