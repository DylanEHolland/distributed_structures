import asyncio
from websockets import serve
from argparse import ArgumentParser
from distributed_structures import node
from datetime import datetime

ap = ArgumentParser()
ap.add_argument("-p", "--port")
args = ap.parse_args()

port = 8765
if args.port:
    port = args.port

n = node()
async def handler(websocket, port):
    async for message in websocket:
        remote_user = ":".join([str(f) for f in websocket.remote_address])
        print(f"[{datetime.now()}] {remote_user} {message}")
        await websocket.send(message)

async def main():
    async with serve(handler, "localhost", int(port)):
        await asyncio.Future()  # run forever

asyncio.run(main())