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
            for param in function_args:

                if param in kwargs:
                    # Did the user override the default?
                    filtered_kwargs[param] = kwargs[param]

                elif param in self._defaults:
                    # Do we have a clobbering value in the default dict?
                    filtered_kwargs[param] = self._defaults[param]

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
        for attr, value in inspect.getmembers(module):

            # If it's a function, wrap it
            if six.callable(value):
                # Wrap the function in a decorator
                setattr(self, attr, self.__wrap(value))

            # If it's a module, construct a parameterizer to wrap it
            elif isinstance(attr, types.ModuleType):
                # test if this is a submodule of the current module
                submodpath = inspect.getfile(value)

                if os.path.commonprefix([modpath, submodpath]) == modpath:
                    if value not in self._dispatch:
                        # We need to pre-seed the dispatch entry to avoid
                        # cyclic references
                        self._dispatch[value] = None

                        self._dispatch[value] = Preset(value,
                                                       dispatch=self._dispatch,
                                                       defaults=self._defaults)

                    setattr(self, attr, self._dispatch[value])
                else:
                    setattr(self, attr, value)


    def __getitem__(self, param):
        return self._defaults[param]

    def __delitem__(self, param):
        del self._defaults[param]

    def __contains__(self, param):
        return param in self._defaults

    def __setitem__(self, param, value):

        self._defaults[param] = value

    def keys(self):
        return self._defaults.keys()

    def update(self, D):

        self._defaults.update(D)
