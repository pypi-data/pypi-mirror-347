# Load the compiled shared library
from ctypes import c_char_p, c_int, POINTER
import ctypes

from doublylist.structure import ListPtr

lib = ctypes.CDLL("bin/doubly.dll")  # use 'studentlist.dll' on Windows

# Set argument and return types for C functions
lib.createList.restype = ListPtr

lib.addNode.argtypes = [ListPtr, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
lib.removeNode.argtypes = [ListPtr, c_int]
lib.traverseBackward.argtypes = [ListPtr]
lib.listCount.argtypes = [ListPtr]
lib.SearchNode.argtypes = [ListPtr, c_int, c_char_p]
lib.destroyList.argtypes = [ListPtr]
lib.destroyList.restype = ListPtr
lib.searchNumber.argtypes = [ListPtr, c_char_p]
lib.searchNumber.restype = POINTER(c_int)
