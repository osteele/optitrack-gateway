#!/usr/bin/env python

from pathlib import Path
from time import sleep
import asyncio
import websockets
import json

HOSTNAME = "localhost"
PORT_NUMBER = 8765

data_dir = Path("./build")
data_path = sorted(data_dir.glob("*.json"))[0]
records = json.load(data_path.open())
print(f"Serving data from {data_path.name} ({len(records)} rows)")


async def echo(websocket, path):
    async for message in websocket:
        req = json.loads(message)
        ix = req["cursor"]
        ix %= len(records)
        print("request", ix, "/", len(records))
        row = records[ix]
        await websocket.send(json.dumps(row))


start_server = websockets.serve(echo, HOSTNAME, PORT_NUMBER)

print(f"Serving ws://{HOSTNAME}:{PORT_NUMBER}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
