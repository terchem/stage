import math
import pandas as pd
from typing import List
#MODULE
#OUTDATED intial attemp was to sort sym equiv. atoms by radial distance
def sym(coord_lines: List[str], tol: float = 1e-4) -> pd.DataFrame:
    reps, radii = [], []

    for line in coord_lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        atom = parts[0]
        x, y, z = map(float, parts[1:4])
        r = math.hypot(x, y)
        if all(abs(r - r0) >= tol for r0 in radii):
            reps.append({'atom': atom, 'x': x, 'y': y, 'z': z, 'r': r})
            radii.append(r)

    df = pd.DataFrame(reps)
    df_sorted = df.sort_values('r').reset_index(drop=True)

    # Print the distances
    print("Saved radial distances:")
    for r in df_sorted['r']:
        print(f"{r:.6f}")

    return df_sorted.drop(columns=['r', 'atom'])
