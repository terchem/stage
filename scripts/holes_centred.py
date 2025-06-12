#from ring_center import ring
import re
import pandas as pd
import numpy as np
from bare_flake import bare
from hyd_flake import hyd
from center_H import add_h


center = np.array([0., 0., 0.])
n = int(input("Define a peremiter n="))
m = int(input("Define a complete mol m="))

nC = 6*m**2
nH = 6*m
natom = nC+nH

coordinates = bare(n)

coord = {
    'x':[],
    'y':[],
    'z':[]
}
for elem in coordinates:
    numb = re.findall("[-+]?(?:\d*\.*\d+)",elem)
    coord['x'].append(numb[0])
    coord['y'].append((numb[1]))
    coord['z'].append((numb[2]))

df = pd.DataFrame.from_dict(coord)
df = df.astype(float)

# Compute distances
df['distance'] = np.linalg.norm(df[['x', 'y', 'z']].values - center, axis=1)

# Get 12 closest atoms excluding center
closest = df[df['distance'] > 0].nsmallest(12, 'distance').copy()

# Sort to make sure distances are in order
closest = closest.sort_values('distance').reset_index(drop=True)

# Split into two groups by distance threshold
# Assume first distance value is one group, then find where it changes
tol = 1e-3
split_idx = np.argmax(~np.isclose(closest['distance'], closest['distance'][0], atol=tol))

group1 = closest.iloc[:split_idx]
group2 = closest.iloc[split_idx:]


group1 = group1.drop(['distance'], axis = 1)
group2 = group2.drop(['distance'], axis = 1)

closest_lis1 = group1.values.tolist()
closest_lis2 = group2.values.tolist()


#print(closest_lis2)

coordinates = hyd(m)


def parse(line):
    parts = line.split()
    return tuple(map(float, parts[1:]))  # skip the first column (like '21')

def match(c1, c2, tol=1e-6):
    return all(abs(a - b) < tol for a, b in zip(c1, c2))


for coord in closest_lis1:
    coordinates = [line for line in coordinates if not match(parse(line), coord)]


for coord in closest_lis2:
    H1, H2, H3 = add_h(center, coord)
    print(H3)
    coordinates.append(("H    " + "    ".join(f"{v:.6f}" for v in H3)))


## write xyz file

outFile = open("graphene-C" + str(nC) + "H" + str(nH) + ".xyz", 'w')
outFile.write(str(natom) + "\n")
outFile.write("Graphene C" + str(nC) + "H" + str(nH) + " in xyz format\n")
for point in coordinates:
    outFile.write(point + "\n")

outFile.close()

