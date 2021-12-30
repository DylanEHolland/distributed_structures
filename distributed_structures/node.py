from os import environ, mkdir
from os.path import exists

class node:
    data_dir = f"{environ.get('HOME')}/dd_node"
    def __init__(self):
        if not exists(self.data_dir):
            mkdir(self.data_dir)
    
    def list(self, name):
        pass