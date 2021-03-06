# (C) Copyright 2017 by Rocky Bernstein
"""
CPython 2.7 bytecode opcodes

This is a like Python 2.7's opcode.py with some classification
of stack usage.
"""

from xdis.opcodes.base import (
    def_op, compare_op, finalize_opcodes,
    init_opdata, jabs_op, jrel_op, name_op, rm_op)
import xdis.opcodes.opcode_26 as opcode_26

version = 2.7

l = locals()
init_opdata(l, opcode_26, version)

# Below are opcode changes since Python 2.6
rm_op(l, 'BUILD_MAP',     104)
rm_op(l, 'LOAD_ATTR',     105)
rm_op(l, 'COMPARE_OP',    106)
rm_op(l, 'IMPORT_NAME',   107)
rm_op(l, 'IMPORT_FROM',   108)
rm_op(l, 'JUMP_IF_FALSE', 111)
rm_op(l, 'EXTENDED_ARG',  143)
rm_op(l, 'JUMP_IF_TRUE',  112)

def_op(l, 'LIST_APPEND',            94, 2, 1) # Calls list.append(TOS[-i], TOS).
                                              # Used to implement list comprehensions.
def_op(l, 'BUILD_SET',             104)       # Number of set items
def_op(l, 'BUILD_MAP',             105)
name_op(l, 'LOAD_ATTR',            106)
compare_op(l, 'COMPARE_OP',        107)

name_op(l, 'IMPORT_NAME',          108,  2,  1)  # Index in name list
name_op(l, 'IMPORT_FROM',          109,  0,  1)

jabs_op(l, 'JUMP_IF_FALSE_OR_POP', 111) # Target byte offset from beginning of code
jabs_op(l, 'JUMP_IF_TRUE_OR_POP',  112)  # ""
jabs_op(l, 'POP_JUMP_IF_FALSE',    114)  # ""
jabs_op(l, 'POP_JUMP_IF_TRUE',     115)  # ""
jrel_op(l, 'SETUP_WITH',           143,  0,  2)

def_op(l, 'EXTENDED_ARG', 145)
def_op(l, 'SET_ADD', 146)
def_op(l, 'MAP_ADD', 147)

# FIXME remove (fix uncompyle6)
def updateGlobal():
    globals().update({'PJIF': l['opmap']['POP_JUMP_IF_FALSE']})
    globals().update({'PJIT': l['opmap']['POP_JUMP_IF_TRUE']})
updateGlobal()

finalize_opcodes(l)
