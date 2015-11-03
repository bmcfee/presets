#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''Presets provides an object interface to a module which can override
the default parameter values.

This is primarily useful for packages which contain many functions with overlapping
parameter sets.  Presets can be used to consistently override all defaults at once,
while maintaining the same externally-facing API.

Example
-------
This example shows how to override common default parameters in the librosa package.

>>> import librosa as _librosa
>>> from presets import Preset
>>> librosa = Preset(_librosa)
>>> librosa['sr'] = 44100
>>> librosa['n_fft'] = 4096
>>> librosa['hop_length'] = 1024
>>> y, sr = librosa.load(librosa.util.example_audio_file())
>>> stft = librosa.stft(y)
>>> tempo, beats = librosa.beat.beat_track(y)
'''

import inspect
import os
import six
import types

from .version import version as __version__

class Preset(object):
    '''The Preset class overrides the default parameters of functions within a module.

    If the given module contains submodules, these are also encapsulated by Preset objects
    that share the same default parameter dictionary.

    Submodules are detected by examining common prefixes of the module source paths.

    Attributes
    ----------
    module : Python module
        The module to encapsulate

    dispatch : None or dictionary
        A dictionary mapping modules to existing Preset objects.
        This should be left as `None` for most situations.

    defaults : None or dictionary
        An existing dictionary object used to collect default parameters.
        Note: this will be passed by reference.
    '''

    def __wrap(self, func):
        '''This decorator overrides the default arguments of a function.

        For each keyword argument in the function, the decorator first checks
        if the argument has been overridden by the caller, and uses that value instead if so.

        If not, the decorator consults the Preset object for an override value.

        If both of the above cases fail, the decorator reverts to the function's native
        default parameter value.
        '''

        def deffunc(*args, **kwargs):
            '''The decorated function'''
            # Get the list of function arguments
            if hasattr(inspect, 'signature'):
                # Python 3.5
                function_args = inspect.signature(func).parameters

            else:
                function_args = inspect.getargspec(func).args

            # Construct a dict of those kwargs which appear in the function
            filtered_kwargs = kwargs.copy()

            # look at all relevant keyword arguments for this function
            for param in function_args:

                if param in kwargs:
                    # Did the user override the default?
                    filtered_kwargs[param] = kwargs[param]

                elif param in self._defaults:
                    # Do we have a clobbering value in the default dict?
                    filtered_kwargs[param] = self._defaults[param]

            # Call the function with the supplied args and the filtered kwarg dict
            return func(*args, **filtered_kwargs) # pylint: disable=W0142

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
            elif isinstance(value, types.ModuleType):
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
        '''Returns a list of currently set parameter defaults'''
        return self._defaults.keys()

    def update(self, D):
        '''Updates the default parameter set by a dictionary D'''
        self._defaults.update(D)
