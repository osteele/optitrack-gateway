import json
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm, trange

csv_dir = Path("data")
json_dir = Path("build")

EXCERPTS = False

# from https://gist.github.com/cbwar/d2dfbc19b140bd599daccbe0fe925597
def sizeof_fmt(num, suffix="B"):
    magnitude = int(math.floor(math.log(num, 1024)))
    val = num / math.pow(1024, magnitude)
    if magnitude > 7:
        return "{:.1f}{}{}".format(val, "Yi", suffix)
    return "{:3.1f}{}{}".format(
        val, ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"][magnitude], suffix
    )


def multi_index_labels(index):
    return [{l[i] for l in index} for i in range(len(index[0]))]


csv_paths = [
    p
    for p in sorted(csv_dir.glob("*.csv"), key=lambda f: f.stat().st_size)
    if "-excerpt" not in p.name
]
if EXCERPTS:
    csv_paths = sorted(csv_dir.glob("*-excerpt.csv"), key=lambda f: f.stat().st_size)

for csv_path in csv_paths:
    print(f"File: {csv_path.name} ({sizeof_fmt(csv_path.stat().st_size)} bytes):")
    df = pd.read_csv(csv_path, header=[0, 1, 3, 4], index_col=0, skiprows=2)
    dfd = df.dropna(1, how="all")
    # print(multi_index_labels(df.columns)[
    #     0], '->', multi_index_labels(dfd.columns)[0])
    print(f"  {len(df.columns)} -> {len(dfd.columns)} columns")
    print(f"  {len(df)} rows")

    poses = []

    for ir, _ in zip(dfd.iterrows(), trange(len(dfd), leave=False)):
        _, row = ir
        part_names = {k[0] for k in row["Bone"].keys()}
        keypoints = [
            {
                "part": k.split(":")[1],
                "score": 1,
                "position": {
                    k.lower(): v for k, v in row["Bone"][k]["Position"].items()
                },
            }
            for k in part_names
            if not any(map(np.isnan, row["Bone"][k]["Position"]))
        ]
        poses.append({"score": 1, "keypoints": keypoints})

    json_path = (json_dir / csv_path.name).with_suffix(".json")
    with json_path.open("w") as f:
        json.dump(poses, f)
    print(f"  -> {json_path} ({sizeof_fmt(json_path.stat().st_size)} bytes)")
