from os import environ, mkdir
from os.path import exists
import asyncio
from websockets import connect
import websockets

class node:
    data_dir = f"{environ.get('DIS_DS_DAEMON_PATH')}/"
    
    def __init__(self):
        self.peers_dir = f"{self.data_dir}/peers"
        if not exists(self.data_dir):
            mkdir(self.data_dir)

        if not exists(self.peers_dir):
            mkdir(self.peers_dir)
            
    def list(self, name):
        pass
    
class client:
    socket = None
    socket_url = None
    
    def __init__(self):
        self.socket_url = "ws://localhost:8765"
        
    def send(self, payload):
        async def hello(uri):
            async with connect(uri) as websocket:
                await websocket.send(payload)
                await websocket.recv()
                # for f in dir(websocket):
                #     if "__" not in f:
                #         print(f)

        asyncio.run(hello(self.socket_url))