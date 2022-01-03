from distributed_structures.block import block
from os import environ, mkdir
from os.path import exists, isfile
from json import loads, dumps

class ledger:
        
    def __init__(self, dirname = None):
        if not dirname:
            print("No ledger dir")
            exit(-1)
        
        ledger_dir = dirname
        self.leafs = {}
        if not exists(ledger_dir):
            mkdir(ledger_dir)
            mkdir(ledger_dir + "/blocks")
            self.head = None
        else:
            with open(f"{ledger_dir}/HEAD", 'r') as fp:
                self.head = loads(fp.read())
                fp.close()
                
            
            fname = f"{ledger_dir}/blocks/{self.head}.json"
            while isfile(fname):
                with open(fname, 'r') as fp:
                    leaf = block().from_serialized(fp.read())
                    fp.close()
                    
                self.leafs[leaf.hash()] = leaf
                if not leaf.next:
                    fname = False
                fname = f"{ledger_dir}/blocks/{leaf.next}.json"
        
    def __del__(self):
        ledger_dir = environ.get("LDR_DIR")
        with open(f"{ledger_dir}/HEAD", 'w') as fp:
            fp.write(dumps(self.head))
            fp.close()
            
        for l in self.leafs:
            FNAME = f"{ledger_dir}/blocks/{l}.json"
            leaf = self.leafs[l]
            with open(FNAME, 'w') as fp:
                fp.write(leaf.serialize())
                fp.close()
            
    def __str__(self):
        buffer = [self.leafs[k].value for k in self.leafs]
        return str(buffer)
            
    def add(self, x):
        b = block()
        b.value = x
        
        self.leafs[b.hash()] = b
        if not self.head:
            self.head = b.hash()
        else:
            node = self.leafs[self.head]
            while node.next in self.leafs:
                node = self.leafs[node.next]
                print(node)
                
            node.next = b.hash()
        
        return b
    
    
#
#
#

class distributed_ledger:
    pass