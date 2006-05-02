# -*- coding: utf-8 -*-
# Copyright 2006 St James Software

__all__ = ['IterativeTester','Dimension']

def combinations(*args):
    """Generate all combinations of items from argument lists.
    """
    if len(args) == 0:
        yield []
    else:
        for x in args[0]:
            for rest in combinations(*args[1:]):
                yield [x] + rest

class IterativeTesterMetaClass(type):
   def __init__(cls, name, bases, dct):
        """We need to create the new test methods at class creation time so that
           py.test knows can find them as soon as the module is loaded."""
        super(IterativeTesterMetaClass, cls).__init__(name, bases, dct)
        cls.makeIterativeTests(dct)

class IterativeTester(object):
    """
    Parent class for test classes which want to have methods iterated over
    sets of parameters.
    """
    
    __metaclass__ = IterativeTesterMetaClass
    
    # Dictionary defining iterative tests. Keys are the prefixes of the
    # methods to be iterated with different parameters. Values are arrays
    # of Dimension objects which need to be iterated over.
    DIMENSIONS = {}
    
    @classmethod
    def makeIterativeTests(cls,dct):
        """
        Create all iterative tests specified in DIMENSIONS dictionary and
        remove processed methods.
        """
        for prefix in cls.DIMENSIONS.keys():
            for methname, meth in dct.iteritems():
                if methname.startswith(prefix) and callable(meth):
                    cls.makeIterativeTestsForMethod(prefix,methname,meth)
                                        
    @classmethod    
    def makeIterativeTestsForMethod(cls,prefix,methname,meth):
        """
        Create the iterative tests for a single method.
        """
        for varnames in cls.permuteVars(prefix):
            cls.createTestMethod(prefix,varnames,methname,meth)
                
    @classmethod
    def createTestMethod(cls,prefix,varnames,oldmethname,oldmeth):
        """
        Add a new test method.
        """
        newname = "test" + oldmethname[len(prefix):] + "_" + "_".join(varnames)
        
        # don't overwrite existing methods
        if cls.__dict__.has_key(newname):
            return

        def newmeth(self):
            args = [dim.getValue(name) for name, dim in zip(varnames,cls.DIMENSIONS[prefix])]
            return oldmeth(self,*args)

        newmeth.func_name = newname
        newmeth.func_doc = oldmeth.func_doc
        newmeth.func_dict = oldmeth.func_dict
                
        setattr(cls,newname,newmeth)

    @classmethod
    def permuteVars(cls,prefix):
        for varnames in combinations(*[dim.getNames() for dim in cls.DIMENSIONS[prefix]]):
            yield varnames

    @classmethod
    def setup_class(cls):
        for prefix, dims in cls.DIMENSIONS.iteritems():
            for dim in dims:
                dim.setup()
                
            setupmeth = getattr(cls,"setup_class_" + prefix,None)
            if callable(setupmeth):
                for varnames in cls.permuteVars(prefix):
                    args = [dim.getValue(name) for name, dim in zip(varnames,cls.DIMENSIONS[prefix])]
                    setupmeth(*args)
                
                
    @classmethod
    def teardown_class(cls):
        for prefix, dims in cls.DIMENSIONS.iteritems():
            for dim in dims:
                dim.teardown()
                
            teardownmeth = getattr(cls,"setup_class_" + prefix,None)
            if callable(teardownmeth):
                for varnames in cls.permuteVars(prefix):
                    args = [dim.getValue(name) for name, dim in zip(varnames,cls.DIMENSIONS[prefix])]
                    teardownmeth(*args)


class Dimension(object):
    """A collection of resources (databases, webservers or whatever) for
       IterativeTesters to access. Sub-classes need to override .getNames()
       to provide a list of names for the available resources and .getValue()
       to allow the resource associated with a name to be fetched. Overriding
       setup and teardown is optional.
       
       For convenience, .getNames() and .getValue() return the resources and
       names from a name <-> resource diciontary held in self._resources, but
       sub-classes should feel free to override these if necessary.
    """

    def getNames(self):
        """Return the names of the resources this Dimension object holds.
           Must be callable as soon as the object has been created.
        """
        return self._resources.keys()
    
    def getValue(self,name):
        """Return the value of a named resource.
           Need only be callable after the objects .setup() method has been called.
        """
        return self._resources[name]
        
    def setup(self):
        """Setup the held resources.
           Does nothing by default.
        """
        pass
        
    def teardown(self):
        """Clean-up and release the held resources.
           Does nothing by default.
        """
        pass
