# Implementation Example

Python wrapper for a C doubly linked list implementation

``` python from src.node_list import NodeList

if __name__ == '__main__':
    sl = NodeList()
    sl.add("49643", "Brs", "Arg1", "Arge", "Expert")
    sl.add("51722", "Sl", "Dev", "Arge", "Mid")
    sl.show_reverse()
    sl.search(no="49643")
    sl.count()
    sl.remove(1)
    sl.count()
    sl.destroy() ```
