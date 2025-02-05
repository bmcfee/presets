#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Presets provides an object interface to a module which can override \
the default parameter values.

This is primarily useful for packages which contain many functions with
overlapping parameter sets.  Presets can be used to consistently override
all defaults at once, while maintaining the same externally-facing API.

Example
-------
This example shows how to override common default parameters in the
librosa package.

>>> import librosa as _librosa
>>> from presets import Preset
>>> librosa = Preset(_librosa)
>>> librosa['sr'] = 44100
>>> librosa['n_fft'] = 4096
>>> librosa['hop_length'] = 1024
>>> y, sr = librosa.load(librosa.util.example_audio_file())
>>> stft = librosa.stft(y)
>>> tempo, beats = librosa.beat.beat_track(y)
"""

import inspect
import os
import types

import functools


short_version = '1.0'
version = '1.0.0'
__version__ = version


class Preset(object):
    """The Preset class overrides the default parameters of functions \
    within a module.

    If the given module contains submodules, these are also encapsulated by
    Preset objects that share the same default parameter dictionary.

    Submodules are detected by examining common prefixes of the module
    source paths.

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
    """

    def __wrap(self, func):
        """Override the default arguments of a function.

        For each keyword argument in the function, the decorator first checks
        if the argument has been overridden by the caller, and uses that value
        instead if so.

        If not, the decorator consults the Preset object for an override value.

        If both of the above cases fail, the decorator reverts to the
        function's native default parameter value.
        """

        def deffunc(*args, **kwargs):
            """Decorate the given function."""
            # Get the list of function arguments
            function_args = inspect.signature(func).parameters

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

            # Call with the supplied args and the filtered kwarg dict
            return func(*args, **filtered_kwargs)  # pylint: disable=W0142

        wrapped = functools.update_wrapper(deffunc, func)

        # force-mangle the docstring here
        wrapped.__doc__ = (
            'WARNING: this function has been modified by the Presets '
            'package.\nDefault parameter values described in the '
            f'documentation below may be inaccurate.\n\n{wrapped.__doc__}')
        return wrapped

    def __init__(self, module, dispatch=None, defaults=None):
        """Initialize Preset object around a given module."""
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
            if callable(value):
                # Wrap the function in a decorator
                wrapped = self.__wrap(value)

                setattr(self, attr, wrapped)

            # If it's a module, construct a parameterizer to wrap it
            elif (isinstance(value, types.ModuleType) and
                  hasattr(value, '__file__')):
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
        """Implement dictionary interface (get) to presets object."""
        return self._defaults[param]

    def __delitem__(self, param):
        """Implement dictionary interface (del) to presets object."""
        del self._defaults[param]

    def __contains__(self, param):
        """Implement dictionary interface (in) to presets object."""
        return param in self._defaults

    def __setitem__(self, param, value):
        """Implement dictionary interface (set) to presets object."""
        self._defaults[param] = value

    def keys(self):
        """Return a list of currently set parameter defaults."""
        return self._defaults.keys()

    def update(self, D):
        """Update the default parameter set with the provided dictionary D."""
        self._defaults.update(D)
