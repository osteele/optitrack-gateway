import json
import math
import os
from pathlib import Path

import click
import numpy as np
import pandas as pd
from tqdm import tqdm, trange

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


def convert_file(csv_path, print_bones=False):
    df = pd.read_csv(
        csv_path,
        header=[0, 1, 3, 4],
        index_col=0,
        skiprows=2,
        nrows=10 if print_bones else None,
    )
    if print_bones:
        bones = {
            col[1].split(":", 2)[1]
            for col in df.columns
            if col[0] == "Bone" and col[2] == "Position"
        }
        print("Bones =", " ".join(sorted(bones)))
        return

    dfd = df.dropna(1, how="all")
    # print(multi_index_labels(df.columns)[0], "->", multi_index_labels(dfd.columns)[0])
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


@click.command()
@click.option(
    "--excerpts", is_flag=True, help="Process the *--excerpt files in FILE_OR_DIR"
)
@click.option(
    "--print-bones", is_flag=True, help="Print the bone names instead of creating JSON"
)
@click.argument("FILE_OR_DIR", nargs=-1, type=click.Path(exists=True))
def convert_all(file_or_dir, excerpts, print_bones):
    ctx = click.get_current_context()
    options = dict(print_bones=print_bones)
    if not file_or_dir:
        ctx.fail("Required at least one FILE_OR_DIR")
    for path in map(Path, file_or_dir):
        if path.is_dir():
            csv_paths = sorted(
                path.glob("*-excerpt.csv")
                if excerpts
                else [p for p in path.glob("*.csv") if "-excerpt" not in p.name],
                key=lambda f: f.stat().st_size,
            )

            for path in csv_paths:
                print(f"File: {path} ({sizeof_fmt(path.stat().st_size)} bytes):")
                convert_file(path, **options)
        elif path.suffix == ".csv":
            convert_file(path, **options)
        else:
            ctx.fail(f"Unknown file type: {path}")


if __name__ == "__main__":
    convert_all()
