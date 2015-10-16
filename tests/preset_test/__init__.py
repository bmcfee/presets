#!/usr/bin/env python

# Import an external module with a default kwarg
import pickle

# Import a submodule
from . import submod
from . import secondmod

def mult(a, b=3):

    return a * b
