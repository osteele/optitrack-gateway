#!/usr/bin/env python

import asyncio
import json
from pathlib import Path
from time import sleep

import websockets
from websockets.exceptions import ConnectionClosedError

HOSTNAME = "localhost"
PORT_NUMBER = 8765

data_dir = Path("./build")
data_paths = sorted(
    p for p in data_dir.glob("*.json") if not p.stem.endswith("-excerpt")
)
data_path = data_paths[0]

records = json.load(data_path.open())
print(f"Serving data from {data_path.name!r} ({len(records)} rows)")


async def handler(websocket, path):
    try:
        async for message in websocket:
            req = json.loads(message)
            ix = req["frame_no"] % len(records)
            # print("request", ix, "/", len(records))
            data = {
                "frame_count": len(records),
                "frame_number": ix,
                "pose": records[ix],
            }
            await websocket.send(json.dumps(data))
    except ConnectionClosedError:
        print("Client closed connection")


print(f"Serving ws://{HOSTNAME}:{PORT_NUMBER}")
start_server = websockets.serve(handler, HOSTNAME, PORT_NUMBER)
asyncio.get_event_loop().run_until_complete(start_server)
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print("Shutting down")
    pass
