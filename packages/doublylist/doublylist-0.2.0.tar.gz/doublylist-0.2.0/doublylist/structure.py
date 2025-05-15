# Define LIST struct
from ctypes import Structure, c_int

from _ctypes import POINTER

from doublylist.node import NodePtr


class List(Structure):
    _fields_ = [
        ('count', c_int),
        ('head', NodePtr),
        ('rear', NodePtr),
    ]


ListPtr = POINTER(List)
