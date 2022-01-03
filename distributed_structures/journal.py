from distributed_structures.journal_block import journal_block
from json import dumps
from distributed_structures.subroutines import hash_string

class journal:
    def __new__(cls, *data, **args):
        self = object.__new__(cls)
        self.head = None
        self.tail = None
        self.__init__(self, *data, **args)
        return self

    def __init__(self, *data, **args):
        self.leafs = {}
        self.head = None
        self.tail = None

    def __str__(self):
        return "<>"

    def all(self, **args):
        n = -1
        if args.get('n'):
            n = args.get('n')

        key = self.head
        entries = []
        counter = 0
        while key in self.leafs:
            leaf_node = self.leafs[key]
            entries.append(leaf_node)
            key = leaf_node.next
            if n > 0 and counter >= n:
                break
            counter += 1

        return entries

    def digest(self):
        return hash_string(self.serialize())

    def entry(self, block):
        if block.data_digest() not in self.leafs:
            if not self.head:
                self.head = block.data_digest()

            if not self.tail:
                self.tail = block.data_digest()
            else:
                block.previous = self.tail
                self.tail = block.data_digest()
            
            if block.previous in self.leafs:
                self.leafs[block.previous].next = block.data_digest()

            self.leafs[block.data_digest()] = block
            

    def serialize(self):
        entries = []
        for row in self.all():
            entries.append(row.serialize(data_only=True))
        return dumps(entries)

    