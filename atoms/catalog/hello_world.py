#! /usr/bin/env python3
#
# hello_world.py
#
"""
A basic demo for how to use the OpenCog AtomSpace together with python,
to store and retreive data. A great place to start for beginners.
"""

from opencog.atomspace import AtomSpace
from opencog.atomspace import types
from opencog.type_constructors import *


space = AtomSpace()
set_default_atomspace(space)

f = ConceptNode("myfile")
n = NumberNode("42")

print("Hey yo its", Link(f,n))

