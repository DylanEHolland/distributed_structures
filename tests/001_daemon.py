#!/usr/bin/env python3
from argparse import ArgumentParser
from distributed_structures import client


ap = ArgumentParser()
ap.add_argument("-p", "--port")
args = ap.parse_args()

port = 8765
if args.port:
    port = args.port
    
def test_client_init():
    c = client()
    c.send("test")
    
if __name__ == "__main__":
    test_client_init()