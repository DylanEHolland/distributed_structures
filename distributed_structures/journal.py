from distributed_structures.journal_block import journal_block
from json import dumps, loads
from distributed_structures.subroutines import hash_string
from uuid import uuid4
from os.path import exists, isfile
from os import mkdir, listdir

class journal:
    def __new__(cls, *data, **args):
        self = object.__new__(cls)

        self.leafs = {}
        self.head = None
        self.tail = None

        self.__init__(self, *data, **args)
        if args.get('from_dir'):
            self.from_dir(args.get('from_dir'))
        else:
            self.uuid = uuid4().hex
            self.head = None
            self.tail = None
            self.journal_dir = args.get('journal_dir') if args.get('journal_dir') else f"/tmp/journal-{self.uuid}"
            self.head_file = f"{self.journal_dir}/head"
            self.tail_file = f"{self.journal_dir}/tail"
            self.leafs_dir = f"{self.journal_dir}/leafs"

        return self

    def __str__(self):
        return f"<Journal [Merkel Tree]: {self.digest()}>"

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

    def from_dir(self, directory):
        if not exists(directory):
            raise Exception()

        self.journal_dir = directory
        self.head_file = f"{self.journal_dir}/head"
        self.tail_file = f"{self.journal_dir}/tail"
        self.leafs_dir = f"{self.journal_dir}/leafs"

        with open(self.head_file, 'r') as fp:
            self.head = loads(fp.read())
            fp.close()

        with open(self.tail_file, 'r') as fp:
            self.tail = loads(fp.read())
            fp.close()

        leaf_files = [f for f in listdir(self.leafs_dir) if ".json" in f]
        for leaf_file in leaf_files:
            leaf_file = f"{self.leafs_dir}/{leaf_file}"
            if isfile(leaf_file):
                with open(leaf_file, 'r') as fp:
                    jb = journal_block(from_dict=loads(fp.read()))
                    fp.close()

                if leaf_file.split("/")[-1].replace(".json", "") != jb.digest():
                    print("Digests don't match")
                    exit(-1)

                self.leafs[jb.digest()] = jb
            

    def serialize(self):
        entries = []
        for row in self.all():
            entries.append(row.serialize(data_only=True))
        return dumps(entries)

    def size(self):
        return len(self.leafs)

    def write(self):
        if not exists(self.journal_dir):
            mkdir(self.journal_dir)

        if not exists(self.leafs_dir):
            mkdir(self.leafs_dir)

        if not isfile(self.head_file):
            with open(self.head_file, 'w') as fp:
                fp.write(dumps(self.head))

        if not isfile(self.tail_file):
            with open(self.tail_file, 'w') as fp:
                fp.write(dumps(self.tail))

        key = self.head
        while key in self.leafs:
            leaf = self.leafs[key]
            fname = f"{self.leafs_dir}/{leaf.digest()}.json"
            with open(fname, 'w') as fp:
                fp.write(leaf.serialize())
                fp.close()

            key = leaf.next
        
    