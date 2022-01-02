from os import environ, mkdir
from os.path import exists
import asyncio
from websockets import connect
import asyncio
from websockets import serve
from datetime import datetime
from json import dumps, loads

class node:
    data_dir = f"{environ.get('DIS_DS_DAEMON_PATH')}/"
    port = 8675
    
    def __init__(self, **args):
        self.peers_dir = f"{self.data_dir}/peers"
        self.lists_dir = f"{self.data_dir}/lists"
        self.lists = {}
        
        if 'port' in args:
            self.port = int(args.get('port'))
        
        if not exists(self.data_dir):
            mkdir(self.data_dir)

        if not exists(self.peers_dir):
            mkdir(self.peers_dir)
            
        if not exists(self.lists_dir):
            mkdir(self.lists_dir)            
            
    def list(self, name):
        pass
    
    def run(self):
        async def handler(websocket, port):
            async for message in websocket:
                remote_user = ":".join([str(f) for f in websocket.remote_address])
                print(f"[{datetime.now()}] {remote_user} {message}")
                output = {
                    'request': message,
                    'response': None
                }
                output['response'] = self.lists
                await websocket.send(dumps(output))

        async def main():
            async with serve(handler, "localhost", int(self.port)):
                await asyncio.Future()  # run forever

        print(asyncio.run(main()))
        
class client:
    socket = None
    socket_url = None
    dlists = {}
    
    def __init__(self):
        self.socket_url = "ws://localhost:8765"
        self.connect()
        
    def connect(self):
        response = self.send("[INIT_CONNECTION]")
        self.dlists = response['response']
        
    def dlist(self, name):
        if name not in self.dlists:
            print("Maybe creating")
            self.send("[GET_LISTS]")
        
    def send(self, payload):
        async def hello(uri):
            async with connect(uri) as websocket:
                await websocket.send(payload)                        
                return await websocket.recv()

        result = asyncio.run(hello(self.socket_url))
        return loads(result)