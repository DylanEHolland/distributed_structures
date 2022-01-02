from argparse import ArgumentParser
from distributed_structures import node

ap = ArgumentParser()
ap.add_argument("-p", "--port")
args = ap.parse_args()

port = 8765
if args.port:
    port = args.port

n = node(port=port)
n.run()
