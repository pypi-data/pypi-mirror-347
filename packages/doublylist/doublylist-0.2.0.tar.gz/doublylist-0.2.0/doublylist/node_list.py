# Python-friendly wrapper class
from doublylist.lib import lib


class NodeList:
    def __init__(self):
        self.list = lib.createList()

    def add(self, no, prefix, suffix, sector, classs):
        lib.addNode(self.list, no.encode(), prefix.encode(), suffix.encode(), sector.encode(), classs.encode())

    def remove(self, index):
        lib.removeNode(self.list, index)

    def show_reverse(self):
        lib.traverseBackward(self.list)

    def count(self):
        lib.listCount(self.list)

    def search(self, index=-1, no="-1"):
        lib.SearchNode(self.list, index, no.encode())

    def find_index(self, no):
        res_ptr = lib.searchNumber(self.list, no.encode())
        return res_ptr[0], bool(res_ptr[1])  # (index, isFound)

    def destroy(self):
        self.list = lib.destroyList(self.list)

    def __del__(self):
        if self.list:
            self.destroy()
