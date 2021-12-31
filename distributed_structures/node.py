from os import environ, mkdir
from os.path import exists

class node:
    data_dir = f"{environ.get('HOME')}/dd_node"
    
    def __init__(self):
        self.peers_dir = f"{self.data_dir}/peers"
        if not exists(self.data_dir):
            mkdir(self.data_dir)

        if not exists(self.peers_dir):
            mkdir(self.peers_dir)
            
    def list(self, name):
        pass