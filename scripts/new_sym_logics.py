
from typing import List

import numpy as np
import pandas as pd


def sym(coord_lines: List[str], tol: float = 1e-4, *, decimals: int = 5) -> pd.DataFrame:

    # parse coordinates
    coords = []
    for line in coord_lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        x, y, z = map(float, parts[1:4])
        coords.append((x, y, z))

    if not coords:
        return pd.DataFrame(columns=["x", "y", "z"])

    # shift to centre of mass
    xy = np.array([(x, y) for x, y, _ in coords])
    xy -= xy.mean(axis=0)

    # build D6h operation set
    OPS = []
    mirror = np.array([[1, 0], [0, -1]])  # reflection across x-axis
    for k in range(6):                    # six 60-degree rotations
        c, s = np.cos(k * np.pi / 3), np.sin(k * np.pi / 3)
        R = np.array([[c, -s],
                      [s,  c]])
        OPS.append(R)           # pure rotation
        OPS.append(R @ mirror)  # rotation followed by reflection

    # pick orbit representatives
    seen   = set()
    keep_i = []

    for idx, v in enumerate(xy):
        orbit = [tuple(np.round(M @ v, decimals)) for M in OPS]
        canon = min(orbit)            # lexicographically minimal image
        if canon not in seen:
            seen.add(canon)
            keep_i.append(idx)

    reps = [coords[i] for i in keep_i]

    # 4. assemble DataFrame, print radii
    df = (pd.DataFrame(reps, columns=["x", "y", "z"])
            .assign(r=lambda d: np.hypot(d.x, d.y))
            .sort_values("r")
            .reset_index(drop=True))

    print("Saved radial distances:")
    for r in df["r"]:
        print(f"{r:.6f}")

    return df.drop(columns="r")
