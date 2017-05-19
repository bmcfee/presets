#!/usr/bin/env python

import presets
import preset_test


def test_main_default():

    P = presets.Preset(preset_test)
    assert preset_test.mult(4) == P.mult(4)


def test_submod_default():
    P = presets.Preset(preset_test)

    assert preset_test.submod.add(4) == P.submod.add(4)


def test_main_override():
    b = -3

    P = presets.Preset(preset_test)
    P['b'] = b
    assert preset_test.mult(4, b=b) == P.mult(4)


def test_submod_override():
    b = -3

    P = presets.Preset(preset_test)
    P['b'] = b
    assert preset_test.submod.add(4, b=b) == P.submod.add(4)


def test_main_update():
    b = -3
    P = presets.Preset(preset_test)
    P['b'] = b
    assert preset_test.mult(4, b=b) == P.mult(4)
    P['b'] = b + 10
    assert preset_test.mult(4, b=b+10) == P.mult(4)


def test_user_override():
    b = -3

    P = presets.Preset(preset_test)
    P['b'] = b
    assert preset_test.mult(4, b=10 + b) == P.mult(4, b=10 + b)


def test_revert():
    b = -3

    P = presets.Preset(preset_test)
    P['b'] = b
    del P['b']
    assert preset_test.mult(4) == P.mult(4)


def test_contains():

    P = presets.Preset(preset_test)
    P['b'] = 3

    assert 'b' in P
    assert 'c' not in P


def test_set_get():

    b = 20
    P = presets.Preset(preset_test)
    P['b'] = b

    assert P['b'] == b


def test_update():

    P = presets.Preset(preset_test)

    params = dict(b=30, c=20, d=50)
    P.update(params)

    for key in params.keys():
        assert P[key] == params[key]


def test_keys():

    P = presets.Preset(preset_test)

    params = dict(b=30, c=20, d=50)
    P.update(params)

    assert set(P.keys()) == set(params.keys())


def test_external():
    P = presets.Preset(preset_test)

    assert preset_test.pickle == P.pickle


def test_docstring():

    P = presets.Preset(preset_test)
    assert 'WARNING' in P.mult.__doc__
