.. presets documentation master file, created by
   sphinx-quickstart on Fri Oct 16 13:55:12 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

presets
=======

Presets provides an object interface that can override common default parameter settings
for all functions within a target module or package.

It's simple to use.  Simply construct a ``Preset`` object with the target module as an argument, then set the
default parameters via a dict-like interface.  After that, your new object will act just as the target module,
but it replaces the default arguments of any functions with values that you set.

Example
-------

.. code-block:: python

    >>> import librosa as _librosa
    >>> from presets import Preset
    >>> librosa = Preset(_librosa)
    >>> librosa['sr'] = 44100
    >>> librosa['n_fft'] = 4096
    >>> librosa['hop_length'] = 1024
    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> sr
    44100
    >>> stft = librosa.stft(y)


API Reference
-------------
.. toctree::
    :maxdepth: 3

    api

Contribute
----------
- `Issue Tracker <http://github.com/bmcfee/presets/issues>`_
- `Source Code <http://github.com/bmcfee/presets>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

