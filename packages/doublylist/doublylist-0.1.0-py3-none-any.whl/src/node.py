from ctypes import Structure, c_char, POINTER


# Define NODE struct
class Node(Structure):
    pass


NodePtr = POINTER(Node)

Node._fields_ = [
    ('Number', c_char * 12),
    ('Prefix', c_char * 12),
    ('Suffix', c_char * 12),
    ('Sector', c_char * 12),
    ('Class',  c_char * 12),
    ('Forw', NodePtr),
    ('backw', NodePtr),
]









