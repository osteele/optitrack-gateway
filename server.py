#!/usr/bin/env python

import asyncio
import json
import re
import sys
from fnmatch import fnmatch
from pathlib import Path
from time import sleep

import click
import websockets
from websockets.exceptions import ConnectionClosedError


def load_bones(path):
    """Return a list of pairs of joints to use as bones."""

    def get_joint_pairs(rig_path):
        """Given a path of the form "a -> b -> c", return a set of tuples
        {("a", "b"), ("b", "c")}.
        """
        joints = re.split(r"\s*->\s*", rig_path)
        return set(zip(joints, joints[1:]))

    config_file = Path("./config.json")
    with config_file.open() as fp:
        config = json.load(fp)

    file_config = next(
        (
            obj
            for obj in config
            if any(fnmatch(config_file, pattern) for pattern in obj["files"])
        ),
        None,
    )
    assert file_config, f"{config_file} has no entry that matches {path!r}"

    bones = set()
    for rig_path in config[0]["rigging"]:
        if "[LR]" in rig_path:
            bones |= get_joint_pairs(rig_path.replace("[LR]", "L"))
            bones |= get_joint_pairs(rig_path.replace("[LR]", "R"))
        else:
            bones |= get_joint_pairs(rig_path)

    return list(bones)


def make_handler(data_path):
    bones = list(load_bones(data_path))
    with Path(data_path).open() as fp:
        records = json.load(fp)
    print(f"Serving data from {data_path!r} ({len(records)} rows)")

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
                    "part_pairs": bones,
                }
                await websocket.send(json.dumps(data))
        except ConnectionClosedError:
            print("Client closed connection")

    return handler


@click.command()
@click.option("--hostname", default="localhost")
@click.option("--port", default=8765)
@click.argument("JSON_PATH", type=click.Path(exists=True))
def serve(json_path, hostname, port):
    handler = make_handler(json_path)
    start_server = websockets.serve(handler, hostname, port)
    print(f"Serving ws://{hostname}:{port}")
    asyncio.get_event_loop().run_until_complete(start_server)
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        pass


if __name__ == "__main__":
    serve()
