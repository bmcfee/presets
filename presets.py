#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''Presets provides an object interface to a module which can override the default parameter values.


'''

import inspect
import os
import six
import types

__version__ = '0.0.1'

class Preset(object):
    
    def __wrap(self, func):
    
        def deffunc(*args, **kwargs):
            
            # Get the list of function arguments
            function_args = inspect.getargspec(func).args
            
            # Construct a dict of those kwargs which appear in the function
            filtered_kwargs = {}
            
            # look at all relevant keyword arguments for this function
            for kw in function_args:
                
                # Do we have a clobbering value in the default dict?
                if kw in self._defaults:
                    filtered_kwargs[kw] = self._defaults[kw]
                    
                # Did the user override all defaults?
                if kw in kwargs:
                    filtered_kwargs[kw] = kwargs[kw]
                    
            # Call the function with the supplied args and the filtered kwarg dict
            return func(*args, **filtered_kwargs)
        
        return deffunc
    
    def __init__(self, module, dispatch=None, defaults=None):
        
        # This defaults directory will get passed around by reference
        if defaults is None:
            defaults = dict()
            
        self._defaults = defaults
        
        self._module = module
        
        if dispatch is None:
            dispatch = dict()
            dispatch[module] = self
            
        self._dispatch = dispatch
        
        
        modpath = os.path.dirname(inspect.getfile(module))
        
        # inspect the target module
        for k, v in inspect.getmembers(module):
            
            # If it's a function, wrap it
            if six.callable(v):
                # Wrap the function in a decorator
                setattr(self, k, self.__wrap(v))
                
            # If it's a module, construct a parameterizer to wrap it
            elif isinstance(v, types.ModuleType):
                # test if this is a submodule of the current module
                submodpath = inspect.getfile(v)
                
                if os.path.commonprefix([modpath, submodpath]) == modpath:
                    if v not in self._dispatch:
                        # We need to pre-seed the dispatch entry to avoid cyclic dependencies
                        self._dispatch[v] = None
                        
                        self._dispatch[v] = Preset(v,
                                                   dispatch=self._dispatch,
                                                   defaults=self._defaults)

                    setattr(self, k, self._dispatch[v])
                else:
                    setattr(self, k, v)
                
        
    def __getitem__(self, key):
        return self._defaults[key]
    
    def __delitem__(self, key):
        del self._defaults[key]
            
    def __contains__(self, key):
        return key in self._defaults
    
    def __setitem__(self, key, value):
        
        self._defaults[key] = value
        
    def keys(self):
        return self._defaults.keys()
    
    def update(self, D):
        
        for k, v in six.iteritems(D):
            self._defaults[k] = v
