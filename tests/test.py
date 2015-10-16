#!/usr/bin/env python

from nose.tools import eq_

import presets
import preset_test


def test_main_default():

    P = presets.Preset(preset_test)
    eq_(preset_test.mult(4), P.mult(4))


def test_submod_default():
    P = presets.Preset(preset_test)

    eq_(preset_test.submod.add(4), P.submod.add(4))


def test_main_override():
    b = -3

    P = presets.Preset(preset_test)
    P['b'] = b
    eq_(preset_test.mult(4, b=b), P.mult(4))


def test_submod_override():
    b = -3

    P = presets.Preset(preset_test)
    P['b'] = b
    eq_(preset_test.submod.add(4, b=b), P.submod.add(4))


def test_main_update():
    b = -3
    P = presets.Preset(preset_test)
    P['b'] = b
    eq_(preset_test.mult(4, b=b), P.mult(4))
    P['b'] = b + 10
    eq_(preset_test.mult(4, b=b+10), P.mult(4))

def test_external():
    P = presets.Preset(preset_test)

    eq_(preset_test.pickle, P.pickle)
